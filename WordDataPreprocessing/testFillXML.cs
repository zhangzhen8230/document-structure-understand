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
using System.Windows.Forms;
namespace DataPreprocessing
{
    class testFillXML
    {
        string keyWord;//关键字
        string fontName;//字体
        float fontSize;//字号
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
        string paraLowerText;//文本内容
        string paraFullText;//段落下文本内容

        public string Fill(ArrayList pathWord,System.Windows.Forms.RichTextBox richTextBoxTest)
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
               
                    string directoryName = System.IO.Path.GetDirectoryName(pathWord[pathWord_i].ToString());
                    directoryName = directoryName.Substring(0, directoryName.LastIndexOf("\\"));
                    string fileNameWithoutExtension = System.IO.Path.GetFileNameWithoutExtension(pathWord[pathWord_i].ToString());
                    //string testDir = directoryName + "\\extractFromWordTxt\\" + fileNameWithoutExtension + ".txt";
                    string testDir = @"E:\Users\zhangzhen\PycharmProjects\document\docreconstruct2\data\test.txt";
                    StreamWriter sw = new StreamWriter(testDir);//将控制台输出写入txt文件
                    Console.SetOut(sw);
                    Console.WriteLine("等号\t关键字\t字体\t字号\t字形\t字数\t编号\t编号位置\tword对象\t行距\t缩进\t段前距\t段后距\t对齐方式\t大纲级别\t标点\t中文比例\t邮箱符号");
                    //打开word文档
                    object openPathWord = pathWord[pathWord_i];
                    doc = app.Documents.Open(ref openPathWord, ref confirmConversions, ref readOnly, ref addToRecentFiles, ref passwordDocument, ref passwordTemplate,
                        ref revert, ref writePasswordDocument, ref writePasswordTemplate, ref format, ref encoding, ref visible, ref openConflictDocument, ref openAndRepair,
                        ref documentDirection, ref noEncodingDialog);
                    Word.Paragraphs paragraphs = doc.Paragraphs;//获得段落集合
                    Dictionary<string, Dictionary<float, int>> relativeFontSize = new Dictionary<string, Dictionary<float, int>>();//相对字号
                    //初始化特征
                    initCharacter();
                    //删除所有批注
                    add_table_Comment(doc);
                    richTextBoxTest.AppendText("特征提取开始" + "\n");
                    int pCount = paragraphs.Count;
                    int para_i = 1;
                    for (;para_i <= paragraphs.Count; para_i++)
                    {

                        richTextBoxTest.AppendText("第" + para_i + "/" + pCount + "段" + "\n");
                        Word.Paragraph para = paragraphs[para_i];
                        if (para.Range.Text.Trim() != "")
                        {

                            if (para.Range.Tables.Count == 0)
                            {

                                writeToTxt(para.Range, para, keywordsList, listFormatList, richTextBoxTest);
                            }
                            else 
                            {
                            //   // int para_num_table = para.Range.Comments[1].Scope.Paragraphs.Count;
                                while (paragraphs[para_i].Range.Comments.Count != 1)
                                   para_i++;
                                writeToTxt(paragraphs[para_i].Range.Comments[1].Scope, para, keywordsList, listFormatList, richTextBoxTest);
                                while (paragraphs[para_i].Range.Tables.Count != 0)
                                    para_i++;
                                para_i--;
                            
                                //只处理第一段 其它都略过
                         
                            }
                        }
                    }
                    for (int numAtt = 0; numAtt < 17;numAtt++ )
                        Console.Write("-" + "\t");
                    Console.Write("-");
                    //先关闭打开的文档（注意saveChanges选项）  
                    Object saveChanges = Word.WdSaveOptions.wdSaveChanges;
                    Object originalFormat = Type.Missing;
                    Object routeDocument = Type.Missing;
                    app.Documents.Close(ref saveChanges, ref originalFormat, ref routeDocument);
                    sw.Flush();
                    sw.Close();
            }

            //若已经没有文档存在，则关闭应用程序  
            if (app.Documents.Count == 0)
            {
                app.Quit(Type.Missing, Type.Missing, Type.Missing);
            }

            return "测试文件特征提取完成";
        }
        //将所有的特征写入txt文件中
        public void writeToTxt(Word.Range range, Word.Paragraph para, ArrayList keywordsList, ArrayList listFormatList, System.Windows.Forms.RichTextBox richTextBoxTes)
        {
            paraLowerText = range.Text.ToString().ToLower();
            paraFullText = range.Text.ToString();
            
            //等号特征
            Console.Write(equals_value(paraFullText) + "\t");//输出到txt文件
            //提取关键字               
            Console.Write(keyword_value(keywordsList, paraLowerText) + "\t");//输出到txt文件
            //提取段落字体、字号、字形、字数
            ArrayList value = font_value(range);
            for (int font_i = 0; font_i < value.Count; font_i++)
            {
                Console.Write(value[font_i] + "\t");
            }
            //提取段落编号
            ArrayList bianhao = bianhao_value(range, listFormatList);
            for (int bianhao_i = 0; bianhao_i < bianhao.Count; bianhao_i++)
            {
                Console.Write(bianhao[bianhao_i] + "\t");
            }
            //提取word对象
            Console.Write(wordObject_value(range) + "\t");

            //提取段落行距
            lineSpacing = para.LineSpacing;

            Console.Write(lineSpacing + "\t");
            //提取段落缩进
            firstLineIndent = para.FirstLineIndent;

            Console.Write(firstLineIndent + "\t");
            //提取段前距
            spaceBefore = para.SpaceBefore;

            Console.Write(spaceBefore + "\t");
            //提取段后距
            spaceAfter = para.SpaceAfter;

            Console.Write(spaceAfter + "\t");
            //提取对齐方式
            alignment = para.Alignment.ToString();
            Console.Write(alignment + "\t");
            //提取大纲级别
            outlineLevel = para.OutlineLevel.ToString();

            Console.Write(outlineLevel + "\t");
            //提取标点
            Console.Write(biaodian_value(paraFullText) + "\t");
            //提取批注中英文所占比例
            Console.Write(rate_value(paraFullText.Trim().Replace("\n","")) + "\t");
            //Console.Write(paraFullText + "\t");
            //提取邮箱符号
            Console.WriteLine(get_contain_at(paraFullText));

        }
        //初始化特征
        public void initCharacter() {
            wordObject = "null";//word对象
            string chRate = "null";
            keyWord = "null";//关键字

            fontName = "";//字体
            fontSize = 0;//字号

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
        }
        //删除批注给表格添加批注
        public void add_table_Comment(Word.Document doc)
        {
            //由于每次删除一个批注后，批注的位置和数量就变了，所以每次都删除第一个。
            int comments_num = doc.Comments.Count;
             for (int i = 1; i <= comments_num; i++)
             {
                 doc.Comments[1].Delete();

             }
             doc.Save();
             ArrayList tablelist = new ArrayList();
             for (int tablePos = 1; tablePos <= doc.Tables.Count; tablePos++)
             {
                 Word.Table nowTable = doc.Tables[tablePos];
                 nowTable.Range.Comments.Add(nowTable.Range, "表格");
             }
           }
        //等号特征
        public string equals_value(String paraFullText)
        {
            equals = false;
            foreach (Match match in Regex.Matches(paraFullText, "="))
            {
                if (match.Value == "=")
                {
                    equals = true;
                    break;
                }
                else
                    break;

            }
            return equals+"";
        }
        //关键字特征
        public string keyword_value(ArrayList keywordsList, String paraLowerText)
        {
            for (int keywordsList_i = 0; keywordsList_i < keywordsList.Count; keywordsList_i++)
            {
                Regex title = (Regex)keywordsList[keywordsList_i];
                if (title.IsMatch(paraLowerText))//正则表达式匹配
                {
                    Match match = title.Match(paraLowerText);
                    keyWord = Regex.Replace(match.Groups[0].Value.Replace(" ", ""), @"\d", "");//获取匹配中的字符串                        
                    break;
                }
                else keyWord = "null";
            }
            keyWord = keyWord.Replace("\n", "").Replace(" ", "").Replace("\t", "").Replace("\r", "");
            keyWord = keyWord.Trim();
            return keyWord;
        }
        //字形，字号，字体，字数
        public ArrayList font_value(Word.Range range) {
            ArrayList value = new ArrayList();
            Dictionary<string, int> fontNameDiction = new Dictionary<string, int>();
            Dictionary<float, int> fontSizeDiction = new Dictionary<float, int>();
            Dictionary<string, int> fontTypeDiction = new Dictionary<string, int>();
            Word.Sentences paraSentences = range.Sentences;
            for (int paraSentences_i = 1; paraSentences_i <= paraSentences.Count; paraSentences_i++)
            {

                fontName = paraSentences[paraSentences_i].Font.Name;//当前句字体
                if (fontName.Equals("")) fontName = paraSentences[paraSentences_i].Characters[1].Font.Name;
                fontSize = paraSentences[paraSentences_i].Font.Size;//当前句字号
                if (fontSize == 9999999) fontSize = paraSentences[paraSentences_i].Characters[1].Font.Size;
                fontType = paraSentences[paraSentences_i].Font.Bold.ToString();//当前句字形
                if (fontType.Equals("9999999")) fontType = paraSentences[paraSentences_i].Characters[1].Font.Bold.ToString();

                if (!fontName.Equals("") && fontNameDiction.ContainsKey(fontName))//将字体添加到字体字典,并记录该字体数量
                {
                    fontNameDiction[fontName] += 1;
                }
                else if (!fontName.Equals(""))
                {
                    fontNameDiction.Add(fontName, 1);
                }
                if (fontSize != 9999999 && fontSizeDiction.ContainsKey(fontSize))//将字号添加到字体字典,并记录该字体数量
                {
                    fontSizeDiction[fontSize] += 1;
                }
                else if (fontSize != 9999999)
                {
                    fontSizeDiction.Add(fontSize, 1);
                }
                if (!fontType.Equals("9999999") && fontTypeDiction.ContainsKey(fontType))//将字形添加到字体字典,并记录该字体数量
                {
                    fontTypeDiction[fontType] += 1;
                }
                else if (!fontType.Equals("9999999"))
                {
                    fontTypeDiction.Add(fontType, 1);
                }
            }
            int countFontName = 0;//统计数量最多的字体
            foreach (string fontname in fontNameDiction.Keys)
            {
                if (fontNameDiction[fontname] >= countFontName)
                {
                    countFontName = fontNameDiction[fontname];
                    fontName = fontname;//数量最多字体
                }
            }
            int countFontSize = 0;//统计数量最多的字号
            foreach (float fontsize in fontSizeDiction.Keys)
            {
                if (fontSizeDiction[fontsize] >= countFontSize)
                {
                    countFontSize = fontSizeDiction[fontsize];
                    fontSize = fontsize;//数量最多字号
                }
            }
            int countFontType = 0;//统计数量最多的字形
            foreach (string fonttype in fontTypeDiction.Keys)
            {
                if (fontTypeDiction[fonttype] >= countFontType)
                {
                    countFontType = fontTypeDiction[fonttype];
                    fontType = fonttype;//数量最多字形
                }
            }
            //提取段落字数
            if (paraSentences.Count == 1)
            {
                sentencesCount = 1;
            }
            else if (paraSentences.Count > 1)
            {
                sentencesCount = 0;
            }
            value.Add(fontName.Replace(" ", ""));
            value.Add(fontSize);
            value.Add(fontType);
            value.Add(sentencesCount);
            return value;
        }
        //编号和编号位置特征
        //段落编号
        public ArrayList bianhao_value(Word.Range range, ArrayList listFormatList)
        {
            ArrayList bianhao_value = new ArrayList();
            bianhao_value.Clear();
            listNum = "null";
            listNumPos = "null";
            string list_value = range.ListFormat.ListType.ToString();
            if (list_value.Equals("wdListNoNumbering"))//手动编号
            {
                for (int listFormatList_i = 0; listFormatList_i < listFormatList.Count; listFormatList_i++)
                {
                    Regex title = (Regex)listFormatList[listFormatList_i];
                    if (title.IsMatch(paraFullText))//正则表达式匹配
                    {
                        Match match = title.Match(paraFullText);
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
                listNum = range.ListFormat.ListString.ToString();
                listNumPos = "段首";
            }
            else if (list_value.Equals("wdListBullet"))
            {
                listNum = range.ListFormat.ListString.ToString();
                listNumPos = "段首";
            }

            else if (list_value.Equals("wdListOutlineNumbering"))//自动编号
            {
                if (range.ListFormat.ListString.ToString().StartsWith("第"))
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
                    listNum = range.ListFormat.ListString.ToString().Split('.').Length.ToString();
                    listNumPos = "段首";
                }
            }
            else listNum = "null";
            bianhao_value.Add(listNum);
            bianhao_value.Add(listNumPos);
            return bianhao_value;

        }
        //word对象特征
        public string wordObject_value(Word.Range range) {
            wordObject = "null";
            if (range.InlineShapes.Count != 0)
            {

                Word.InlineShape shape = range.InlineShapes[1];

                if (shape.Type == Word.WdInlineShapeType.wdInlineShapePicture && range.Text.Trim().Length <= 2)//判断是否为图片
                {
                    wordObject = "图对象";

                }
                else if (shape.Type == Word.WdInlineShapeType.wdInlineShapeEmbeddedOLEObject && range.Text.Trim().Length <= 2)//判断是否为图片
                {
                    wordObject = "公式对象";
                }
            }
            else if (range.Comments.Count >= 1 && range.Comments[1].Range.Text == "表格")
            {
                wordObject = "表对象";//判断是否为表格
            }
            else if (range.OMaths.Count > 0)
            {
                wordObject = "公式对象";//判断是否为公式对象
            }
            return wordObject;
        }
         //提取标点
        public string biaodian_value(String paraFullText)
        {
            if (paraFullText.Trim().Equals(""))
            {
                punctuation = false;
            }
            else if (char.IsPunctuation(paraFullText.Trim()[paraFullText.Trim().Length - 1]))//句末有标点
            {
                punctuation = true;
            }
            else punctuation = false;
           return punctuation+"";
        }
        //添加中文比例
        public string rate_value(String paraFullText)
        {
            string subscope = "";
            String chRate = "null";
            try
            {
                if (paraFullText.Length < 200)
                {
                    subscope = paraFullText;
                }
                else
                    subscope = paraFullText.Substring(0, 200);

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
                if (chRate == "非数字")
                {
                    chRate = "0";
                }
            }
            catch (Exception e)
            {
                chRate = 1 + "";
            }
            return chRate;
        }
        //邮箱符号
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
        //将段落角色添加到段落中
        public void FillParaId(ArrayList pathWord) {
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
            string  fullPath = @"E:\Users\zhangzhen\PycharmProjects\document\docreconstruct2\data\result.csv";

            StreamReader reader = new StreamReader(fullPath);
            string line = "";
            List<string> listStrArr = new List<string>();//数组List，相当于可以无限扩大的二维数组。
            line = reader.ReadLine();//读取一行数据
            while (line != null)
            {
                listStrArr.Add(line);//将文件内容分割成数组
                line = reader.ReadLine();
            }


            for (int pathWord_i = 0; pathWord_i < pathWord.Count; pathWord_i++)//逐个打开文件夹下文档
            {
                
                string directoryName = System.IO.Path.GetDirectoryName(pathWord[pathWord_i].ToString());
                directoryName = directoryName.Substring(0, directoryName.LastIndexOf("\\"));
                string fileNameWithoutExtension = System.IO.Path.GetFileNameWithoutExtension(pathWord[pathWord_i].ToString());
                //打开word文档
                object openPathWord = pathWord[pathWord_i];
                    doc = app.Documents.Open(ref openPathWord, ref confirmConversions, ref readOnly, ref addToRecentFiles, ref passwordDocument, ref passwordTemplate,
                        ref revert, ref writePasswordDocument, ref writePasswordTemplate, ref format, ref encoding, ref visible, ref openConflictDocument, ref openAndRepair,
                        ref documentDirection, ref noEncodingDialog);
                    //特殊处理表格，先直接判断 添加表格批注
                  app.Visible = true;    
            
                  add_table_Comment(doc);
                  Word.Paragraphs paragraphs = doc.Paragraphs;//获得段落集合
                   for (int i = 1,j=0; i <= paragraphs.Count; i++)
                     {
                         if (paragraphs[i].Range.Text.Trim() != "")
                         {
                             if (i <= listStrArr.Count && paragraphs[i].Range.Tables.Count == 0)
                             {
                                 if (listStrArr[j] == "表格")
                                 {
                                     j++;
                                 }
                                 Word.Range range = paragraphs[i].Range;
                                 splitLabel(listStrArr[j++], range);
                             }
                         }
                        }
                    Object saveChanges = Word.WdSaveOptions.wdSaveChanges;
                    Object originalFormat = Type.Missing;
                    Object routeDocument = Type.Missing;
                    doc.Save();
            }
        }
        public void splitLabel(string label,Word.Range range) {

            switch (label)
            {
                case "英文摘要":
                    //range.Comments.Add(range, label);
                    splitRange(label, range, "(^([\\s]*)abstract([\\s]*)([:|：]*))", "英文摘要标题", "英文摘要内容"); 
                    break;
                case "中文摘要":
                    //range.Comments.Add(range, label);
                    splitRange(label, range, "(^([\\s]*)摘([\\s]*)要([\\s]*)([:|：]*))", "中文摘要标题", "中文摘要内容"); 
                    break;
                case "中文关键词":
                    //range.Comments.Add(range, label);
                    splitRange(label, range, "(^([\\s]*)关([\\s]*)键([\\s]*)(词|字)([\\s]*)([:|：]*))", "中文关键词标题", "中文关键词内容"); 
                    break;
                case "英文关键词":
                    //range.Comments.Add(range, label);
                    splitRange(label, range, "(^([\\s]*)key([\\s]*)words([:|：]*))", "英文关键词标题", "英文关键词内容"); 
                    break;
                case "一级标题":
                    //range.Comments.Add(range, label);
                    splitRange(label, range, "(((^\\d+(\\.\\d+)*)|(^第([\u4e00-\u9fa5]+)章))([.|:]*))", "一级标题编号", "一级标题内容"); 
                    break;
                case "二级标题":
                    //range.Comments.Add(range, label);
                   splitRange(label, range, "(((^\\d+(\\.\\d+)*)|(^第([\u4e00-\u9fa5]+)章))([.|:]*))", "二级标题编号", "二级标题内容");
                    break;
                case "三级标题":
                    //range.Comments.Add(range, label);
                    splitRange(label, range, "(((^\\d+(\\.\\d+)*)|(^第([\u4e00-\u9fa5]+)章))([.|:]*))", "三级标题编号", "三级标题内容");
                    break;
                case "四级标题":
                    //range.Comments.Add(range, label);
                   splitRange(label, range, "(((^\\d+(\\.\\d+)*)|(^第([\u4e00-\u9fa5]+)章))([.|:]*))", "四级标题编号", "四级标题内容");
                    break;
                case "公式":
                    splitRange(label, range, "(([\\(|（]*\\s*\\d*(.|-)\\d+\\s*[\\)|）]*\\s*$)|(\\[*\\s*\\d*(.|-)\\d+\\s*\\]*\\s*$))", "公式编号", "公式内容");
                    break;
                case "姓名":
                    string rate = rate_value(range.Text.Trim());
                    if(float.Parse(rate)>=0.5)
                        range.Comments.Add(range, "中文姓名");
                    else
                        range.Comments.Add(range, "英文姓名");
                    break;
                case "单位":
                    string rate_danwei = rate_value(range.Text.Trim());
                    if (float.Parse(rate_danwei) >= 0.5)
                        range.Comments.Add(range, "中文单位");
                    else
                        range.Comments.Add(range, "英文单位");
                    break;
                case "邮箱":
                    range.Comments.Add(range, label);
                    break;
                case "论文名称":
                     string rate_name = rate_value(range.Text.Trim());
                     if (float.Parse(rate_name) >= 0.5)
                        range.Comments.Add(range, "中文论文名称");
                    else
                        range.Comments.Add(range, "英文论文名称");
        
                    break;
                case "表题":
                    //range.Comments.Add(range, label);
                    splitRange(label, range, "^([\\s]*)表([\\s]*)([0-9]+)([.|-]*)([0-9])", "表题编号", "表题内容"); 
                    break;
                case "图题":
                    splitRange(label, range, "^([\\s]*)图([\\s]*)([0-9]+)([.|-]*)([0-9])", "图题编号", "图题内容");
                    break;
                case "文本段":
                    String pattern = "((^\\((\\d+)\\))|(^\\（(\\d+)\\）)|(^\\d+\\）)|(^\\d+\\)))";
                    Regex list_pattern = (Regex)new Regex(pattern);
                     string list_value = range.ListFormat.ListType.ToString();
                     if (list_value.Equals("wdListNoNumbering"))//手动编号
                     {
                         if (list_pattern.IsMatch(range.Text.ToString().ToLower()))
                         {
                             range.Comments.Add(range, "列表");
                             Match match = list_pattern.Match(range.Text.ToLower());
                             String matchvalue = match.Groups[0].Value; //返回匹配的内容
                             int start1 = range.Start;   //切分后前面部分(例如摘要标题)，range开始的位置
                             int end1 = 0;               //切分后前面部分，range结束的位置
                             int start2 = 0;              //切分后后面部分，range开始的位置
                             int end2 = range.End;       // 切分后后面部分，range结束的位置
                             end1 = start1 + matchvalue.Length;
                             start2 = end1 + 1;
                           //  range.SetRange(start1, end1);
                             range.Comments.Add(range, "列表编号"); //给前半部分标题添加批注
                             //range.SetRange(start2, end2);
                              range.Comments.Add(range, "列表内容");//给后半部分内容添加批注
                         }
                         else
                             range.Comments.Add(range, "文本段");
                     }else
                         range.Comments.Add(range, "列表");
                   
                    break;
                default:
                    range.Comments.Add(range,label);
                    break;
            }
        }
        public void splitRange(string label,Word.Range range, String pattern,String title,String content) {
            int start1 = range.Start;   //切分后前面部分(例如摘要标题)，range开始的位置
            int end1 = 0;               //切分后前面部分，range结束的位置
            int start2 = 0;              //切分后后面部分，range开始的位置
            int end2 = range.End;       // 切分后后面部分，range结束的位置
            Regex abstractch = (Regex)new Regex(pattern);
            if (abstractch.IsMatch(range.Text.ToString().ToLower()))//正则表达式匹配
            {
                Match match = abstractch.Match(range.Text.ToLower());
                String matchvalue = match.Groups[0].Value; //返回匹配的内容
                if (title == "公式编号")
                {
                    end1 = end2 - matchvalue.Length;
                    range.SetRange(start1, end1);
                    range.Comments.Add(range, content); //给前半部分标题添加批注

                    matchvalue = matchvalue.TrimStart();
                    start2 = end2 - matchvalue.Length + 1;
                    range.SetRange(start2, end2);
                    range.Comments.Add(range, title);//给后半部分内容添加批注

                }
                else
                {
                    end1 = start1 + matchvalue.Length;
                    start2 = end1 + 1;
                    range.SetRange(start1, end1);
                    range.Comments.Add(range, title); //给前半部分标题添加批注
                    range.SetRange(start2, end2);
                    range.Comments.Add(range, content);//给后半部分内容添加批注
                }
            }
            else {
                range.Comments.Add(range, content);
            }
        }


    }
}
