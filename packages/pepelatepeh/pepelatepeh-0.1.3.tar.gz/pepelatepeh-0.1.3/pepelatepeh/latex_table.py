def latex_table(table: list):
    begin = '\\begin{tabular}{|'+ 'c|'*len(table[0]) +'}\n'
    rows = '\\hline\n' + '\\hline\n'.join(map(latex_row,table))
    end = '\\hline\n\\end{tabular}\n'
    return begin + rows + end


def latex_row(row: list):
    return ' & '.join(map(str,row)) + ' \\\\\n'


def latex_image(path: str, width: str = "0.5\\textwidth") -> str:
    begin = '\\begin{figure}[h!]\n\\centering\n'
    mid = f'\\includegraphics[width={width}]'+'{' + path + '}\n'
    end = '\\end{figure}\n'
    return begin + mid + end


def latex_doc(table,funk):
    begin = '\\documentclass{article}\n\\usepackage{graphicx}\n\\begin{document}\n'
    end = '\\end{document}'
    return  begin+ funk(table) + end