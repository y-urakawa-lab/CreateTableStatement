# coding: utf-8
import tkinter, tkinter.filedialog, tkinter.messagebox

"""
SQL出力クラス
"""
class SqlWriter:
    def create_table_text(self, raw_data, type_list, length_list):

        is_first = True  # 1行目のフラグ

        table_name = "TableName"
        print_text = ""
        print_text += 'コピーしてご利用ください '
        print_text += '\nWindows:Ctrl+Cでコピー\nMac:多すぎて表示が切れている場合は\n commad+shift押しながら選択\n\n' + 'create table ' + table_name + ' (\n'

        """
        取得した配列の中に一つでもstrがあったら文字列
        str > datatime > date time > int で決定
        
        varchar : 256 >= mediumtext
                  
        int : 10 > 7 > 0 でbigint int(10) int(1>) 
        """
        for (column, typename, m) in zip(raw_data.columns, type_list, length_list):

            if 'str' in str(typename):
                if m >= 256:
                    output_column = "`" + str(column) + "` mediumtext"
                else:
                    output_column = "`" + str(column) + "` varchar(" + str(m) + ")"

            elif 'datetime' in str(typename):
                output_column = "`" + str(column) + "` datetime"
            elif 'date' in str(typename):
                output_column = "`" + str(column) + "` date"
            elif 'time' in str(typename):
                output_column = "`" + str(column) + "` time"

            elif 'int' in str(typename):
                if m >= 10:
                    output_column = "`" + str(column) + "` bigint(" + str(m) + ")"
                elif m >= 7:
                    output_column = "`" + str(column) + "` int(" + str(10) + ")"
                else:
                    output_column = "`" + str(column) + "` int(" + str(m) + ")"

            elif 'char' in str(typename):
                output_column = "`" + str(column) + "` char"

            elif 'float' in str(typename):
                if "" in str(typename):
                    output_column = "`" + str(column) + "` varchar(256)"
                else:
                    output_column = "`" + str(column) + "` double"
            else:
                output_column = "NA"

            # 頭に「,」つけるか否か
            if (is_first):
                print_text += output_column + '\n'
                is_first = False
            else:
                print_text += "," + output_column + '\n'

        print_text += ');\n\n'

        tkinter.messagebox.showinfo('TypeChecker', print_text)
        return


        


