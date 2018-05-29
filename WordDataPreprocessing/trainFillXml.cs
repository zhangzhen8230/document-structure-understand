using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Xml;
using Word = Microsoft.Office.Interop.Word;

namespace DataPreprocessing
{
    class trainFillXml
    {

        string keyWord;//关键字
        string keyWordFontType;//关键字字形
        string keyWordFontPos;//关键字位置
        string fontName;//字体
        float fontSize;//字号
        float maxFontSize;//最大字号
        float minFontSize;//最小字号       
        float textFontSize;//正文字号
        int sentencesCount;//字数
        string fontType;//字形
        string fontColor;//颜色
        string listNum;//编号
        string wordObject;//word对象
        string listNumPos;//编号位置
        float lineSpacing;//行距
        float firstLineIndent;//缩进
        float spaceBefore;//段前距
        float spaceAfter;//段后距
        string alignment;//对齐方式
        string outlineLevel;//大纲级别
        bool punctuation;//段尾标点
        bool equals;//等号

        public string Fill(ArrayList pathWord, ArrayList pathXml)
        {

            Word.Application app = new Microsoft.Office.Interop.Word.Application(); //可以打开word程序,程序是Application
            Word.Document doc = null; //一会要记录word打开的文档,打开word文档和word程序不是一回事,文档是document
            //设置打开文档参数
            Object confirmConversions = Type.Missing;
            Object readOnly = Type.Missing;
            Object addToRecentFiles = Type.Missing;
            Object passwordDocument = Type.Missing;
            Object passwordTemplate = Type.Missing;
            Object revert = Type.Missing;
            Object writePasswordDocument = Type.Missing;
            Object writePasswordTemplate = Type.Missing;
            Object format = Type.Missing;
            Object encoding = Type.Missing;
            Object visible = Type.Missing;
            Object openConflictDocument = Type.Missing;
            Object openAndRepair = Type.Missing;
            Object documentDirection = Type.Missing;
            Object noEncodingDialog = Type.Missing;

            XmlDocument xmlDoc = new XmlDocument();//读入xml

            //匹配关键字正则表达式
            ArrayList keywordsList = new ArrayList();
            keywordsList.Add(new Regex("(^([\\s]*)摘([\\s]*)要([\\s]*))"));//正则表达式——摘要
            keywordsList.Add(new Regex("(^([\\s]*)abstract)"));//正则表达式——摘要
            keywordsList.Add(new Regex("(^([\\s]*)关([\\s]*)键([\\s]*)字)"));//正则表达式——关键字
            keywordsList.Add(new Regex("(^([\\s]*)关([\\s]*)键([\\s]*)词)"));//正则表达式——关键词
            keywordsList.Add(new Regex("(^([\\s]*)key([\\s]*)words)"));//正则表达式——关键词
            keywordsList.Add(new Regex("^([\\s]*)图([\\s]*)([0-9]*)"));//正则表达式——图题
            keywordsList.Add(new Regex("^([\\s]*)表([\\s]*)([0-9]*)"));//正则表达式——表题
            //匹配编号正则表达式
            ArrayList listFormatList = new ArrayList();
            //公式编号
            listFormatList.Add(new Regex("(\\((\\d+(.\\d+)?)\\)([\\s]*)$)"));
            listFormatList.Add(new Regex("(\\（(\\d+(.\\d+)?)\\）([\\s]*)$)"));
            //列表编号
            listFormatList.Add(new Regex("(^\\((\\d+)\\))"));
            listFormatList.Add(new Regex("(^\\（(\\d+)\\）)"));
            listFormatList.Add(new Regex("(^\\d+\\）)"));
            listFormatList.Add(new Regex("(^\\d+\\))"));
            //标题编号
            listFormatList.Add(new Regex("(^\\d+(\\.\\d+)*)"));
            listFormatList.Add(new Regex("(^第([\u4e00-\u9fa5]+)章)"));

            for (int pathWord_i = 0; pathWord_i < pathWord.Count; pathWord_i++)//逐个打开文件夹下文档
            {
                try
                {
                    string directoryName = System.IO.Path.GetDirectoryName(pathWord[pathWord_i].ToString());
                    directoryName = directoryName.Substring(0, directoryName.LastIndexOf("\\"));
                    string fileNameWithoutExtension = System.IO.Path.GetFileNameWithoutExtension(pathWord[pathWord_i].ToString());
                    //打开word文档
                    object openPathWord = pathWord[pathWord_i];
                    doc = app.Documents.Open(ref openPathWord, ref confirmConversions, ref readOnly, ref addToRecentFiles, ref passwordDocument, ref passwordTemplate,
                        ref revert, ref writePasswordDocument, ref writePasswordTemplate, ref format, ref encoding, ref visible, ref openConflictDocument, ref openAndRepair,
                        ref documentDirection, ref noEncodingDialog);
                    Word.Comments comments = doc.Comments;//获得word文档批注集合
                    //打开xml文档
                    string openPathXml = (string)pathXml[pathWord_i];
                    xmlDoc.Load(openPathXml); //加载xml文件
                    XmlNodeList nodeList = xmlDoc.SelectNodes("//node()[@index]");//找到有index属性的节点集合
                    string indexValue = "index";
                    //Console.WriteLine(extractDoc[extractDoc_i]);//文档名称
                    XmlNamespaceManager nameSpace = new XmlNamespaceManager(xmlDoc.NameTable);
                    nameSpace.AddNamespace("xslw", "http://www.bistu.edu.cn/document_processing/corpus/academic_paper");
                    nameSpace.AddNamespace("xsi", "http://www.w3.org/2001/XMLSchema-instance");

                    Dictionary<string, Dictionary<float, int>> relativeFontSize = new Dictionary<string, Dictionary<float, int>>();//相对字号
                    //初始化特征
                    wordObject = "null";//word对象
                    string chRate = "null";
                    keyWord = "null";//关键字
                    keyWordFontType = "null";//关键字字形
                    keyWordFontPos = "null";//关键字位置
                    fontName = "";//字体
                    fontSize = 0;//字号
                    maxFontSize = 0;//最大字号
                    minFontSize = 9999999;//最小字号,提取不出的字号为9999999
                    textFontSize = 0;//正文字号
                    sentencesCount = 0;//字数
                    fontType = "null";//字形
                    fontColor = "null";//颜色
                    listNum = "null";//编号
                    wordObject = "null";//word对象
                    listNumPos = "null";//编号位置
                    lineSpacing = 12;//行距
                    firstLineIndent = 0;//缩进
                    spaceBefore = 0;//段前距
                    spaceAfter = 0;//段后距
                    alignment = "null";//对齐方式
                    outlineLevel = "null";//大纲级别
                    punctuation = false;//段尾标点
                    equals = false;//内容中是否含有等号
                    ArrayList tablelist = new ArrayList();
                    tablelist.Clear();
          
                    foreach (XmlNode xmlNode in nodeList)
                    {
                        int commentId = int.Parse(xmlNode.Attributes.GetNamedItem(indexValue).Value);
                        if (commentId <= comments.Count)
                        {
                            if (commentId == 241) {
                                int s = 1;
                            }
                            Word.Comment comment = comments[commentId];
                            //if (comment.Range.Text.Replace(" ","").Equals(xmlNode.Attributes.GetNamedItem("DCL_ID").Value)) {
                            XmlElement xmlElement = (XmlElement)xmlNode;
                            //分别获取每个段落特征
                            string commentText = comment.Range.Text;//批注内容
                            string paraText = comment.Scope.Paragraphs[1].Range.Text;//批注下的段落内容
                            string scopeText = comment.Scope.Text;//批注范围下内容                                                                 
                            equals = false;
                            //提取文本内容
                            if (commentText.Length > 9)
                            {
                                Console.Write(commentText.Substring(0, 9) + "    ");
                            }
                            else Console.Write(commentText + "    ");
                            foreach (Match match in Regex.Matches(paraText, "="))
                            {
                                if (match.Value == "=")
                                {
                                    equals = true;
                                    break;
                                }
                                else
                                    break;

                            }
                            xmlElement.SetAttribute("等号", equals + "");//添加xml节点的格式属性
                            //提取关键字               
                            for (int keywordsList_i = 0; keywordsList_i < keywordsList.Count; keywordsList_i++)
                            {
                                Regex title = (Regex)keywordsList[keywordsList_i];
                                if (title.IsMatch(paraText.ToLower()))//正则表达式匹配
                                {
                                    Match match = title.Match(paraText.ToLower());
                                    keyWord = Regex.Replace(match.Groups[0].Value.Replace(" ", ""), @"\d", "");//获取匹配中的字符串                        
                                    break;
                                }
                                else keyWord = "null";
                            }
                            //Console.Write(keyWord + "    ");//输出关键字
                            xmlElement.SetAttribute("关键字", keyWord);//添加xml节点的格式属性

                            //提取段落字体、字号、字形
                            Dictionary<string, int> fontNameDiction = new Dictionary<string, int>();
                            Dictionary<float, int> fontSizeDiction = new Dictionary<float, int>();
                            Dictionary<string, int> fontTypeDiction = new Dictionary<string, int>();
                            Word.Sentences commSentences = comment.Scope.Sentences;
                            fontName = commSentences[1].Font.Name;//当前句字体
                            if (fontName.Equals("")) fontName = commSentences[1].Characters[1].Font.Name;
                            fontSize = commSentences[1].Font.Size;//当前句字号
                            if (fontSize == 9999999) fontSize = commSentences[1].Characters[1].Font.Size;
                            fontType = commSentences[1].Font.Bold.ToString();//当前句字形
                            if (fontType.Equals("9999999")) fontType = commSentences[1].Characters[1].Font.Bold.ToString();
                            xmlElement.SetAttribute("字体", fontName.Replace(" ", ""));//添加xml节点的格式属性
                            xmlElement.SetAttribute("字号", fontSize.ToString());//添加xml节点的格式属性
                            xmlElement.SetAttribute("字形", fontType);//添加xml节点的格式属性

                            //提取段落字数
                            if (commSentences.Count == 1)
                            {
                                sentencesCount = 1;
                            }
                            else if (commSentences.Count > 1)
                            {
                                sentencesCount = 0;
                            }
                            xmlElement.SetAttribute("字数", sentencesCount.ToString());//添加xml节点的格式属性

                            //提取段落编号
                            string[] bianhaoArray = get_bianhao(comment, paraText, listFormatList);
                            xmlElement.SetAttribute("编号", bianhaoArray[0]);
                            xmlElement.SetAttribute("编号位置", bianhaoArray[1]);

                            //提取word对象
                            if (comment.Scope.InlineShapes.Count != 0)
                            {

                                Word.InlineShape shape = comment.Scope.InlineShapes[1];

                                if (shape.Type == Word.WdInlineShapeType.wdInlineShapePicture && comment.Scope.Text.Trim().Length <= 2)//判断是否为图片
                                {
                                    wordObject = "图对象";

                                }
                                else if (shape.Type == Word.WdInlineShapeType.wdInlineShapeEmbeddedOLEObject && comment.Scope.Text.Trim().Length <= 2)//判断是否为图片
                                {
                                    wordObject = "公式对象";
                                }
                            }
                            else if (tablelist.Contains(comment.Range.Text))
                            {
                                wordObject = "表对象";//判断是否为表格
                            }
                            else if (comment.Scope.OMaths.Count > 0)
                            {
                                wordObject = "公式对象";//判断是否为公式对象
                            }

                            xmlElement.SetAttribute("word对象", wordObject);//添加xml节点的格式属性
                            wordObject = "null";
                            //提取段落行距
                            lineSpacing = comment.Scope.Paragraphs[1].LineSpacing;
                            xmlElement.SetAttribute("行距", lineSpacing.ToString());//添加xml节点的格式属性

                            //提取段落缩进
                            firstLineIndent = comment.Scope.Paragraphs[1].FirstLineIndent;
                            xmlElement.SetAttribute("缩进", firstLineIndent.ToString());//添加xml节点的格式属性

                            //提取段前距
                            spaceBefore = comment.Scope.Paragraphs[1].SpaceBefore;
                            xmlElement.SetAttribute("段前距", spaceBefore.ToString());//添加xml节点的格式属性

                            //提取段后距
                            spaceAfter = comment.Scope.Paragraphs[1].SpaceAfter;
                            xmlElement.SetAttribute("段后距", spaceAfter.ToString());//添加xml节点的格式属性

                            //提取对齐方式
                            alignment = comment.Scope.Paragraphs[1].Alignment.ToString();
                            Console.Write(alignment + "    ");//输出对齐方式
                            xmlElement.SetAttribute("对齐方式", alignment);//添加xml节点的格式属性

                            //提取大纲级别
                            outlineLevel = comment.Scope.Paragraphs[1].OutlineLevel.ToString();
                            xmlElement.SetAttribute("大纲级别", outlineLevel);//添加xml节点的格式属性
                            string contain_at = get_contain_at(scopeText);
                            xmlElement.SetAttribute("邮箱符号", contain_at);
                            //提取标点
                            if (paraText.Trim().Equals(""))
                            {
                                punctuation = false;
                            }
                            else if (char.IsPunctuation(paraText.Trim()[paraText.Trim().Length - 1]))//句末有标点
                            {
                                punctuation = true;
                            }
                            else punctuation = false;
                            xmlElement.SetAttribute("标点", punctuation.ToString());//添加xml节点的格式属性
                            //提取批注中英文所占比例
                            string subscope = "";
                            try
                            {
                                if (scopeText.Length < 200)
                                {
                                    subscope = scopeText;
                                }
                                else
                                    subscope = scopeText.Substring(0, 200);

                                subscope = subscope.Trim();
                                subscope = subscope.Replace("/t", "").Replace("/n", "").Replace(" ", "");

                                float chLen = 0; // 中文长度
                                float enLen = 0;
                                for (int i = 0; i < subscope.Length; i++)
                                {
                                    byte[] byte_len = System.Text.Encoding.Default.GetBytes(subscope.Substring(i, 1));
                                    if (byte_len.Length > 1)
                                        chLen += 1;
                                    else
                                        enLen += 1;
                                }
                                chRate = "" + (chLen / (chLen + enLen));
                            }
                            catch (Exception e)
                            {
                                chRate = 1 + "";
                            }
                            xmlElement.SetAttribute("中文比例", chRate);//添加xml节点的格式属性
                            chRate = "null";
                        }
                    }
                    //保存填充好属性的xml文档
                    string xmlFinallDir = directoryName + "\\xmlFinall\\" + fileNameWithoutExtension + ".xml";
                    xmlDoc.Save(xmlFinallDir);

                    //先关闭打开的文档（注意saveChanges选项）  
                    Object saveChanges = Word.WdSaveOptions.wdDoNotSaveChanges;
                    Object originalFormat = Type.Missing;
                    Object routeDocument = Type.Missing;
                    app.Documents.Close(ref saveChanges, ref originalFormat, ref routeDocument);
     
                    //}
                }
                catch (Exception e)
                {
                    int a = 1;
                }
            }

            //若已经没有文档存在，则关闭应用程序  
            if (app.Documents.Count == 0)
            {
                app.Quit(Type.Missing, Type.Missing, Type.Missing);
            }



            return "属性自动填充完成。";
        }
 
        //段落编号
        public String[] get_bianhao(Word.Comment comment, string paraText, ArrayList listFormatList)
        {
            String[] str = new string[2];
            string listNum = "null";
            string listNumPos = "null";
            string list_value = comment.Scope.Paragraphs[1].Range.ListFormat.ListType.ToString();
            if (list_value.Equals("wdListNoNumbering"))//手动编号
            {
                for (int listFormatList_i = 0; listFormatList_i < listFormatList.Count; listFormatList_i++)
                {
                    Regex title = (Regex)listFormatList[listFormatList_i];
                    if (title.IsMatch(paraText))//正则表达式匹配
                    {
                        Match match = title.Match(paraText);
                        listNum = match.Groups[0].Value.Replace(" ", "").Trim();//获取匹配中的字符串
                        if (title.ToString().Equals("(^第([\u4e00-\u9fa5]+)章)"))
                        {
                            listNum = "1";
                        }
                        else if (title.ToString().Equals("(^\\d+(\\.\\d+)*)"))
                        {
                            listNum = listNum.ToString();
                        }
                        if (title.ToString().Contains("^"))
                        {//获取匹配中字符的位置
                            listNumPos = "段首";
                        }
                        else if (title.ToString().Contains("$"))
                        {
                            listNumPos = "段尾";
                        }
                        break;
                    }
                }
            }
            else if (list_value.Equals("wdListSimpleNumbering"))
            {
                listNum = comment.Scope.Paragraphs[1].Range.ListFormat.ListString.ToString();
                listNumPos = "段首";
            }
            else if (list_value.Equals("wdListBullet"))
            {
                listNum = comment.Scope.Paragraphs[1].Range.ListFormat.ListString.ToString();
                listNumPos = "段首";
            }

            else if (list_value.Equals("wdListOutlineNumbering"))//自动编号
            {
                if (comment.Scope.Paragraphs[1].Range.ListFormat.ListString.ToString().StartsWith("第"))
                {
                    listNum = "1";
                    listNumPos = "段首";
                }
                else if (list_value.ToString().Equals("wdListSimpleNumbering"))
                {
                    listNum = "wdListSimpleNumbering";
                    listNumPos = "段首";
                }
                else if (list_value.Equals("wdListBullet"))
                {
                    listNum = "wdListBullet";
                    listNumPos = "段首";
                }
                else
                {
                    listNum = comment.Scope.Paragraphs[1].Range.ListFormat.ListString.ToString().Split('.').Length.ToString();
                    listNumPos = "段首";
                }
            }
            else listNum = "null";
            str[0] = listNum;
            str[1] = listNumPos;
            return str;

        }
        //判断某一行是否含有@符号
        private string get_contain_at(string scopeText)
        {
            string contain = "0";
            try
            {
                int len = scopeText.Length - 1;

                if (scopeText.Length <= 0)
                {
                    return contain;
                }

                //只取文本内容的前50个字
                if (len >= 50)
                {
                    scopeText = scopeText.Substring(0, 50) + scopeText.Substring(len - 50, 50);
                }
                if (scopeText.Contains("@"))
                    contain = "1";
            }
            catch
            {

            }
            return contain;
        }  
    }
}
