using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.IO;

namespace xmltocsv
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog fbDlg = new FolderBrowserDialog();
            fbDlg.SelectedPath = @"E:\课题\实验\语料xml与word汇总_20180523\学位论文\xmlFinall"; 
            if (fbDlg.ShowDialog() == DialogResult.OK)
            {
                //存储读取的路径
                string myDir = fbDlg.SelectedPath;
                //遍历文件夹内的文件
                String[] extractDoc = new String[System.IO.Directory.GetFiles(myDir).Count()];
               int  index=0;
                foreach (string fileName in System.IO.Directory.GetFiles(myDir))
                {
                    //对各个文件进行操作
                    extractDoc[index] = fileName;
                    index++;
                }
                writetxt wr = new writetxt();
                wr.write(extractDoc);
                MessageBox.Show("转换完成");
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            string path = @"E:\课题\实验\语料xml与word汇总_20180523\学位论文\txt\";  //测试一个word文档
            System.Diagnostics.Process.Start(path); //打开此文件。
        }
    }
}
