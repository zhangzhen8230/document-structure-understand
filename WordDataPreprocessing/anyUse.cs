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
    class anyUse
    {
      
        string wordObject;//word对象
     

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


            for (int pathWord_i = 0; pathWord_i < pathWord.Count; pathWord_i++)//逐个打开文件夹下文档
            {
                    string directoryName = System.IO.Path.GetDirectoryName(pathWord[pathWord_i].ToString());
                    directoryName = directoryName.Substring(0, directoryName.LastIndexOf("\\"));
                    string fileNameWithoutExtension = System.IO.Path.GetFileNameWithoutExtension(pathWord[pathWord_i].ToString());
                    string testDir = directoryName + "\\extractFromWordTxt\\" + fileNameWithoutExtension + ".txt";
                    StreamWriter sw = new StreamWriter(testDir);//将控制台输出写入txt文件
                    Console.SetOut(sw);

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
                    foreach (XmlNode xmlNode in nodeList)
                    {
                        int commentId = int.Parse(xmlNode.Attributes.GetNamedItem(indexValue).Value);
                        if (commentId <= comments.Count)
                        {
                            Word.Comment comment = comments[commentId];
                            //if (comment.Range.Text.Replace(" ","").Equals(xmlNode.Attributes.GetNamedItem("DCL_ID").Value)) {
                            XmlElement xmlElement = (XmlElement)xmlNode;
                            //分别获取每个段落特征
                            string commentText = comment.Range.Text;//批注内容
                            string paraText = comment.Scope.Paragraphs[1].Range.Text;//批注下的段落内容
                            string scopeText = comment.Scope.Text;//批注范围下内容                                                                 

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

                    sw.Flush();
                    sw.Close();
                    //}
                //}
                //catch (Exception e)
                //{
                //    int a = 1;
                //}
            }

            //若已经没有文档存在，则关闭应用程序  
            if (app.Documents.Count == 0)
            {
                app.Quit(Type.Missing, Type.Missing, Type.Missing);
            }



            return "属性自动填充完成。";
        }
    }
}
