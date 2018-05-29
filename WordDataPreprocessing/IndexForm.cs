using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DataPreprocessing
{
    public partial class IndexForm : Form
    {
        public IndexForm()
        {
            InitializeComponent();
        }

        private void 自动填充_Click(object sender, EventArgs e) //训练文件提取特征
        {
            //遍历文档
            string dirXml = textBox1.Text;
            string dirWord = textBox2.Text;           
            DirectoryInfo folderWord = new DirectoryInfo(dirWord);
            DirectoryInfo folderXml = new DirectoryInfo(dirXml);
            ArrayList pathWord = new ArrayList();
            ArrayList pathXml = new ArrayList();
            
            foreach (FileInfo wordfile in folderWord.GetFiles())
            {
                if (wordfile.Name.Substring(0, 2) != "~$")
                {
                    string pathWord_temp = dirWord + "\\" + wordfile.Name;                    
                    string pathWordWithoutExtension = System.IO.Path.GetFileNameWithoutExtension(pathWord_temp);//无后缀的xml文件名                     
                    string pathXml_temp = dirXml + "\\" + pathWordWithoutExtension + ".xml";//判断xml文件夹下是否存在该xml文件
                    if (System.IO.File.Exists(pathXml_temp))
                    {
                        pathXml.Add(pathXml_temp);//xml文档地址
                        pathWord.Add(pathWord_temp);//word文档地址 
                    }
                    else continue;                                    
                }
            }
            trainFillXml fillxml = new trainFillXml();
            string stateOfFillXML = fillxml.Fill(pathWord,pathXml);
            //在状态栏显示自动填充属性完成状态
            toolStripStatusLabel1.Text = stateOfFillXML;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string defaultfilePath = Environment.CurrentDirectory;
            System.Windows.Forms.FolderBrowserDialog folder = new System.Windows.Forms.FolderBrowserDialog();
            //folder.RootFolder = @"E:\\研二\\课题\\程序代码\\DataPreprocessing\\178篇语料";
            if (defaultfilePath != "")
            {
                //设置此次默认目录为上一次选中目录
                folder.SelectedPath = defaultfilePath;
            }
            if (folder.ShowDialog() == DialogResult.OK)
            {
                this.textBox1.Text = folder.SelectedPath;
            }
            
        }

        private void button2_Click(object sender, EventArgs e)                                                                                    
        {
            string defaultfilePath = Environment.CurrentDirectory;
            System.Windows.Forms.FolderBrowserDialog folder = new System.Windows.Forms.FolderBrowserDialog();
            
            if (defaultfilePath != "")
            {
                //设置此次默认目录为上一次选中目录
                folder.SelectedPath = defaultfilePath;
            }
            if (folder.ShowDialog() == DialogResult.OK)
            {
                this.textBox2.Text = folder.SelectedPath;
            }
        }

        private void button7_Click(object sender, EventArgs e)  //测试文件提取特征
        {
            //遍历文档
            string dirWord = textBox3.Text;
            DirectoryInfo folderWord = new DirectoryInfo(dirWord);
            ArrayList pathWord = new ArrayList();

            foreach (FileInfo wordfile in folderWord.GetFiles())
            {
                if (wordfile.Name.Substring(0, 2) != "~$")
                {
                    string pathWord_temp = dirWord + "\\" + wordfile.Name;
                    string pathWordWithoutExtension = System.IO.Path.GetFileNameWithoutExtension(pathWord_temp);//无后缀的xml文件名  
                    pathWord.Add(pathWord_temp);//word文档地址 
                }
            }
            testFillXML fillxml = new testFillXML();
            richTextBoxTest.SelectionStart = richTextBoxTest.Text.Length;
            richTextBoxTest.SelectionLength = 0;
            richTextBoxTest.Focus();
            string stateOfFillXML = fillxml.Fill(pathWord,richTextBoxTest);
            MessageBox.Show(stateOfFillXML);
        } 

        private void button8_Click(object sender, EventArgs e) //添加段落角色
        {
            //遍历文档
            string dirWord = textBox3.Text;
            DirectoryInfo folderWord = new DirectoryInfo(dirWord);
            ArrayList pathWord = new ArrayList();

            foreach (FileInfo wordfile in folderWord.GetFiles())
            {
                if (wordfile.Name.Substring(0, 2) != "~$")
                {
                    string pathWord_temp = dirWord + "\\" + wordfile.Name;
                    string pathWordWithoutExtension = System.IO.Path.GetFileNameWithoutExtension(pathWord_temp);//无后缀的xml文件名  
                    pathWord.Add(pathWord_temp);//word文档地址 
                }
            }

            testFillXML fillxml = new testFillXML();
            fillxml.FillParaId(pathWord);
            //在状态栏显示自动填充属性完成状态
        }

        private void richTextBoxTest_TextChanged(object sender, EventArgs e)
        {
           
        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void button6_Click(object sender, EventArgs e)
        {
            string defaultfilePath = Environment.CurrentDirectory;
            System.Windows.Forms.FolderBrowserDialog folder = new System.Windows.Forms.FolderBrowserDialog();
            //folder.RootFolder = @"E:\\研二\\课题\\程序代码\\DataPreprocessing\\178篇语料";
            if (defaultfilePath != "")
            {
                //设置此次默认目录为上一次选中目录
                folder.SelectedPath = defaultfilePath;
            }
            if (folder.ShowDialog() == DialogResult.OK)
            {
                this.textBox3.Text = folder.SelectedPath;
            }
        }

 

     
    }
}
