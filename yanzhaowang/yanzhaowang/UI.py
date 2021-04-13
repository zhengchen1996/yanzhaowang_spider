import tkinter
from tkinter import ttk
from scrapy import cmdline
import MySQLdb
import yanzhaowang.dialog


class myWin:
    def __init__(self, text):

        self.win = tkinter.Tk()
        self.win.title(text)
        #buildStr = "%dx%d+%d+%d" % (self.height, self.width, self.x, self.y)
        self.win.geometry("1020x350")
        self.win.resizable(0, 0)

        self.schoolNameEntry = tkinter.Entry(self.win, width=15)  # 院校名称
        self.schoolNameEntry.place(x=50, y=10)

        self.locationComboxlist = ttk.Combobox(self.win, width=10)
        self.locationComboxlist["values"] = ("", "北京", "天津", "山西")
        self.locationComboxlist.current(0)
        self.locationComboxlist.place(x=175, y=10)

        self.belongComboxlist = ttk.Combobox(self.win, width=15)
        self.belongComboxlist["values"] = \
            ("", "教育部", "北京市", "天津市", "工业与信息化部", "中央统战部", "中国科学院",
             "国家体育总局", "海关总署", "公安部", "交通运输部", "天津市体育局", "中国民用航空局",
             "国家民族事务委员会", "外交部", "国家卫生健康委员会", "中央办公厅")
        self.belongComboxlist.current(0)
        self.belongComboxlist.place(x=280, y=10)

        self.graduateSchool = ttk.Combobox(self.win, width=5)
        self.graduateSchool["values"] = ("", "是", "否")
        self.graduateSchool.current(0)
        self.graduateSchool.place(x=420, y=10)

        self.optionalComboxlist = ttk.Combobox(self.win, width=5)
        self.optionalComboxlist["values"] = ("", "是", "否")
        self.optionalComboxlist.current(0)
        self.optionalComboxlist.place(x=490, y=10)

        self.typeComboxlist = ttk.Combobox(self.win, width=10)
        self.typeComboxlist["values"] = \
            ("", "教育学", "医学", "文学", "工学", "法学", "哲学", "经济学", "历史学", "理学", "管理学")
        self.typeComboxlist.current(0)
        self.typeComboxlist.place(x=560, y=10)

        self.subjectEntry = tkinter.Entry(self.win, width=30)  # 科目
        self.subjectEntry.place(x=670, y=10)

        self.numberEntry = tkinter.Entry(self.win, width=10)  # 号码
        self.numberEntry.place(x=900, y=10)



        self.searchButton = tkinter.Button(self.win, text="搜索",
                                           command=self.search, width=15)   #searchButton
        self.searchButton.place(x=50, y=300)

        self.spiderButton = tkinter.Button(self.win, text="爬取并更新数据库",
                                           command=self.spider, width=15)  # spiderButton
        self.spiderButton.place(x=800, y=300)

        self.csvButton = tkinter.Button(self.win, text="导出表中.csv",
                                        command=self.csvBuild, width=15)  # csvButton
        self.csvButton.place(x=250, y=300)

        self.tree = ttk.Treeview(self.win, show="headings")  # 表格
        self.tree["columns"] = \
            ("学校名", "所在地", "院校隶属", "研究生院", "自划线院校", "专业分类", "硕士专业", "专业号码")  # 实际相当于字典
        self.tree.column("学校名", width=130)  # 表示列，不显示
        self.tree.column("所在地", width=100, anchor='center')
        self.tree.column("院校隶属", width=140, anchor='center')
        self.tree.column("研究生院", width=75, anchor='center')
        self.tree.column("自划线院校", width=75, anchor='center')
        self.tree.column("专业分类", width=100, anchor='center')
        self.tree.column("硕士专业", width=230, anchor='center')
        self.tree.column("专业号码", width=100, anchor='center')

        self.tree.heading("学校名", text="学校名")  # 显示表头
        self.tree.heading("所在地", text="所在地")
        self.tree.heading("院校隶属", text="院校隶属")
        self.tree.heading("研究生院", text="研究生院")
        self.tree.heading("自划线院校", text="自划线院校")
        self.tree.heading("专业分类", text="专业分类")
        self.tree.heading("硕士专业", text="硕士专业")
        self.tree.heading("专业号码", text="专业号码")
        # self.tree.insert("", 0, text="测试条目", values=("测试条目", "测试条目", "测试条目", "测试条目"))  # 插入的行数
        self.tree.place(x=40, y=50)

    def getKeyList(self):
        keyWordList = list("abcdefgh")
        for i in range(len(keyWordList)):
            keyWordList[i] = ""

        keyWordList[0] = self.schoolNameEntry.get()
        keyWordList[1] = self.locationComboxlist.get()
        keyWordList[2] = self.belongComboxlist.get()
        keyWordList[3] = self.graduateSchool.get()
        keyWordList[4] = self.optionalComboxlist.get()
        keyWordList[5] = self.typeComboxlist.get()
        keyWordList[6] = self.subjectEntry.get()
        keyWordList[7] = self.numberEntry.get()

        return keyWordList

    def sqlBuild(self):
        keyMap = [" schoolName = ", " location = ", " belong = ", " graduateSchool = ",
                  " optional = ", " type = ", " subject = ", " number = "]
        keyList = self.getKeyList()
        flag = 0
        for i in range(len(keyList)):
            if keyList[i] == "":
                flag += 1
            elif i == len(keyList):
                keyList[i] = keyMap[i] + "'" + keyList[i] + "'"
            else:
                keyList[i] = keyMap[i] + "'" + keyList[i] + "'" + " and"

        sqlWhere = \
            (keyList[0] + keyList[1] + keyList[2] + keyList[3] + keyList[4] +
             keyList[5] + keyList[6] + keyList[7]).strip(" and")

        if flag == len(keyList):
            sql = \
            "select schoolName, location, belong, graduateSchool, optional, type, subject, number, url from yanzhaowangList"
        else:
            sql = \
            "select schoolName, location, belong, graduateSchool, optional, type, subject, number, url " \
            "from yanzhaowangList where " + sqlWhere


        return sql
    def search(self):
        self.treeviewClear()
        resultList = self.getConnection()
        self.listToTreeview(resultList)
        self.label.tex
        yanzhaowang.dialog.Dialog("c")

    def csvBuild(self):
        self.index = 0
        self.file = open("研招网选择数据.csv", "w+", encoding="utf-8")
        if self.index == 0:
            column_name = "学校名,所在地,院校隶属,研究生院,自划线院校,专业分类,硕士专业,专业号码,网址\n"
            self.file.write(column_name)
            self.index = 1
        self.file.close()
        treeItems = self.tree.get_children()
        for item in treeItems:
            itemValues = self.tree.item(item, "values")
            self.file = None

            self.file = open("研招网选择数据.csv", "a", encoding="utf-8")

            csvStr = itemValues[0] + "," + itemValues[1] + "," + itemValues[2] + \
                     "," + itemValues[3] + "," + itemValues[4] + "," + itemValues[5] + \
                     "," + itemValues[6] + "," + itemValues[7] + "," + "\n"
            self.file.write(csvStr)
        self.file.close()
        yanzhaowang.dialog.Dialog("b")

    def spider(self):
        cmdline.execute("scrapy crawl date".split())
        yanzhaowang.dialog.Dialog("e")

    #从数据库取得数据
    def getConnection(self):
        dbName = "yanzhaowang"
        host = "localhost"
        user = "root"
        password = "123456"

        self.db_conn = MySQLdb.connect(db=dbName,
                                       host=host,
                                       user=user,
                                       password=password,
                                       charset="utf8")

        self.db_cursor = self.db_conn.cursor()  # 得到游标
        print("得到游标")
        sql = self.sqlBuild()
        print(sql)
        print(type(sql))
        self.db_cursor.execute(sql)
        resultList = self.db_cursor.fetchall()
        self.db_cursor.close()
        self.db_conn.close()
        return resultList

    # 将list内容显示到treeview
    def listToTreeview(self,resultList):
        amount = 0
        for times in range(0, len(resultList)):
            self.tree.insert("", times, text="%d" % times, values=(
                resultList[times][0], resultList[times][1], resultList[times][2], resultList[times][3],
                resultList[times][4], resultList[times][5], resultList[times][6], resultList[times][7]))
            times += 1
            amount += 1
        strLabel = "得到数据条数：" + str(amount)
        label = tkinter.Label(self.win, anchor=tkinter.CENTER,
                              text=strLabel, width=20,
                              height=3)
        label.place(x=500, y=285)
    # 清空当前treeview显示内容
    def treeviewClear(self):
        treeItems = self.tree.get_children()
        for item in treeItems:
            self.tree.delete(item)

    # 运行起来
    def show(self):
        self.win.mainloop()