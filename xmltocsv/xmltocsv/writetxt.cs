using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;
namespace xmltocsv
{
    class writetxt
    {
        XmlDocument xmlDoc = new XmlDocument();//读入xml
        public void write(string[] filepath) {
            string txtpath = @"E:\课题\实验\语料xml与word汇总_20180523\学位论文\txt\traindata.txt";
            StreamWriter sw = new StreamWriter(txtpath);//将控制台输出写入txt文件
            Console.SetOut(sw);
            Console.WriteLine("段落角色\t等号\t关键字\t字体\t字号\t字形\t字数\t编号\t编号位置\tword对象\t行距\t缩进\t段前距\t段后距\t对齐方式\t大纲级别\t标点\t邮箱符号\t中文比例\t文章名称\t文本内容");
            foreach (string path in filepath)
            {
             
                try
                {
                    xmlDoc.Load(path);

                   XmlNode root = xmlDoc.DocumentElement;
                foreach (XmlNode xmlNode in root.ChildNodes)
                {
                    getNodes(xmlNode);

                }
                Console.WriteLine("-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-");
                }
                catch
                {
                    continue;
                }
            }
            sw.Flush();
            sw.Close();
        }

        public void getNodes(XmlNode node)
        {
            String nodeName = node.Name;// 当前节点名称
            XmlAttributeCollection attributes = node.Attributes;  //当前节点的属性
            if(attributes!=null&&attributes.Count>=5){
                foreach (XmlAttribute att in attributes)
                {  //遍历属性
                    if (att.Name == "role"){
                        string roleval = att.Value.ToString().Split('_')[0].Replace("xslw:", "");
                        roleval = roleval.Trim().Replace("\n", "");
                        if (roleval!="中文摘要标题" && roleval != "一级列表开始" && roleval != "二级列表开始" && roleval != "三级列表开始" && roleval != "四级列表开始" &&
                           roleval != "一级列表结束" && roleval != "二级列表结束" && roleval != "三级列表结束" && roleval != "四级列表结束" &&
                          roleval != "英文摘要标题" && roleval != "中文关键字标题" && roleval != "英文关键字标题" && 
                           roleval != "一级标题编号" && roleval != "二级标题编号" && roleval != "三级标题编号" && roleval != "四级标题编号" &&
                            roleval != "英文图题编号" && roleval != "中文图题编号" && roleval != "表题编号" && roleval != "五级标题编号"
                            && roleval != "公式编号" && roleval != "中文关键词标题" && roleval != "英文关键词标题" && roleval != "表题编号" &&
                           roleval != "一级列表编号" && roleval != "二级列表编号" && roleval != "三级列表编号" && roleval != "四级列表编号" &&
                           roleval != "图题编号" && roleval != "英文表题编号" && roleval != "致谢标题编号" && roleval != "中文表格说明" && roleval != "英文表格说明" 
                           &&roleval != "中文图片说明" && roleval != "英文图片说明" && roleval != "英文论文副题目" && roleval != "列表题目"
                             && roleval != "致谢标题" && roleval != "致谢内容" && roleval != "参考文献题目" && roleval != "参考文献标题" && roleval != "参考文献标题编号"
                            && roleval != "参考文献条目" && roleval != "参考文标题编号" && roleval != "列表编号" && roleval != "附录标题" && roleval != "中文论文副题目"
                            && roleval != "附录标题编号" && roleval != "文章编号标题"
                            && roleval != "文献标志码标题" && roleval != "中图分类号内容" && roleval != "中图分类号标题" && roleval != "五级列表开始" && roleval != "五级列表结束"
                            && roleval != "作者简介内容" && roleval != "作者简介标题" && roleval != "五级列表项目" && roleval != "五级列表编号" && roleval != "结束语标题编号"
                            && roleval != "前言或引言标题编号" && roleval != "作者简介标题" && roleval != "五级列表项目" && roleval != "五级列表编号" && roleval != "结束语标题编号")
                        {  //如果含有role或者dclid属性，则将其写入文档中
                            foreach (XmlAttribute att1 in attributes)
                            {  //遍历要写入文档的属性处理之后，写入文档。
                                //if (att1.Name == "id")
                                //{
                                //    Console.Write(att1.Value + "\t");
                                //}
                                if ( att1.Name != "id" && att1.Name != "颜色" && !att1.Name.ToString().Equals( "DCL_ID"))
                                {
                                    if (att1.Name == "index") {
                                       // Console.WriteLine(att1.Value + "\t");
                                    } 
                                  
                                    else if (att1.Name == "role")
                                    {
                                        string role = att1.Value.ToString().Split('_')[0].Replace("xslw:", "");
                                        role = role.Trim();
                                        if (role == "中文摘要内容")
                                        {
                                            Console.Write("中文摘要");
                                        }
                                        else if (role == "英文摘要内容")
                                        {
                                            Console.Write("英文摘要");
                                        }
                                        else if (role == "英文作者"||role=="中文作者")
                                        {
                                            Console.Write("姓名");
                                        }
                                        else if (role == "中文作者单位" || role == "英文作者单位")
                                        {
                                            Console.Write("单位");
                                        }
                                        else if (role == "中文作者邮箱" || role == "英文作者邮箱")
                                        {
                                            Console.Write("邮箱" );
                                        }
                                        else if (role == "英文论文名称" || role == "英文论文题目" || role == "中文论文副题目" || role == "中文论文题目")
                                        {
                                            Console.Write("论文名称");
                                        }
                                        else if (role == "中文关键字内容" || role == "中文关键词内容")
                                        {
                                            Console.Write("中文关键词" );
                                        }
                                        else if (role == "英文关键字内容" || role == "英文关键词内容")
                                        {
                                            Console.Write("英文关键词");
                                        }
                                        else if (role == "一级标题内容" || role == "前言或引言标题内容" || role == "结束语标题")
                                        {
                                            Console.Write("一级标题" );
                                        }
                                        else if ( role == "二级标题内容")
                                        {
                                            Console.Write("二级标题" );
                                        }
                                        else if ( role == "三级标题内容")
                                        {
                                            Console.Write("三级标题" );
                                        }
                                        else if (role == "四级标题内容")
                                        {
                                            Console.Write("四级标题" );
                                        }
                                        else if (role == "五级标题内容")
                                        {
                                            Console.Write("五级标题" );
                                        }
                                        else if (role == "图题内容"||role=="英文图题内容")
                                        {
                                            Console.Write("图题");
                                        }
                                        else if (role == "表题内容"||role=="英文表题内容" )
                                        {
                                            Console.Write("表题" );
                                        }
                                        else if (role == "一级列表项目" || role == "列表" || role == "二级列表项目" || role == "三级列表项目" || role == "四级列表项目")
                                        {
                                            Console.Write("文本段落" );
                                        }

                                        else if (role == "列表内容" || role == "前言或引言内容" || role == "结束语内容")
                                        {
                                            Console.Write("文本段落");
                                        }
                                        else if (role == "中文关键字内容")
                                        {
                                            Console.Write("关键词");
                                        }
                                        else if (role == "公式内容")
                                        {
                                            Console.Write("公式" );
                                        }

                                        else
                                            Console.Write(role );
                                    }
                                    else
                                    {
                                        //string role = att1.Value.ToString().Replace("\t", "").Replace("\n", "").Replace(" ", "");
                                        string role = att1.Value.Replace("\n", "").Replace(" ", "").Replace("　", "").Replace("\t", "").Replace("\r", "").Replace(" ","");
                                        role = role.Trim();
                                        Console.Write( "\t"+role);
                                    }
                                }
                            }
                            Console.WriteLine();
                        }
                       
                    }
                }
            }
            // 递归遍历当前节点所有的子节点  
            XmlNodeList listNode = node.ChildNodes;// 所有一级子节点的list 
            if (listNode.Count > 0)
            {
                foreach (XmlNode e in listNode)
                {// 遍历所有一级子节点  
                    getNodes(e);// 递归  
                }
            }
        }
    }
}
