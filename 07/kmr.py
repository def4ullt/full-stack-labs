"""Міксини для статистики, простих SVG-стовпчиків та порівняння двох КМР."""
from pathlib import Path
from collections import Counter
from statistics import mean
import sys
import webbrowser
from xml.sax.saxutils import escape

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/"05"))
from marks import read_marks,question_stats

class KmrCsv:
    def __init__(self,ref=None,num=1):
        self.num=num
        self.set_ref(ref)
    def set_ref(self,ref):
        self.ref=Path(ref) if ref else None
        self.rows=read_marks(self.ref) if self.ref else []
    def get_ref(self):
        return self.ref
    def set_num(self,num):
        self.num=num
    def read(self):
        self.rows=read_marks(self.ref)
        return self.rows
    def info(self):
        print(self.num,len({r.student for r in self.rows}))

class Statistic:
    def avg_stat(self):
        return tuple(yes for yes,_ in question_stats(self.rows))
    def marks_stat(self):
        return dict(sorted(Counter(r.mark for r in self.rows).items()))
    def marks_per_time(self):
        return {r.student:60*r.mark/r.seconds for r in self.rows if r.seconds}
    def best_marks_per_time(self,bottom_margin=0,top_margin=10):
        candidates=((r.student,r.mark,60*r.mark/r.seconds) for r in self.rows if r.seconds and bottom_margin<=r.mark<=top_margin)
        return tuple(sorted(candidates,key=lambda row:row[2],reverse=True)[:5])

class Plots:
    def set_cat(self,path):
        self.cat=Path(path)
    def chart(self,name,title,items):
        items=list(items)
        self.cat.mkdir(parents=True,exist_ok=True)
        width=125+32*len(items)
        highest=max([v for _,v in items]+[1])
        doc=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="275" font-family="sans-serif"><rect width="100%" height="100%" fill="white"/><text x="14" y="24">{escape(title)}</text>']
        for i,(label,value) in enumerate(items):
            x=22+32*i
            h=145*value/highest
            doc.append(f'<rect x="{x}" y="{207-h}" width="22" height="{h}" fill="#476c92"/><text font-size="9" x="{x}" y="{202-h}">{value:.1f}</text><text font-size="10" x="{x}" y="222">{escape(str(label))}</text>')
        path=self.cat/f"kmr{self.num}_{name}.svg"
        path.write_text("".join(doc)+"</svg>",encoding="utf8")
        return path
    def avg_plot(self,values=None):
        return self.chart("answers","Повністю правильні відповіді, %",enumerate(values if values is not None else self.avg_stat(),1))
    def marks_plot(self,values=None):
        return self.chart("marks","Розподіл оцінок, студентів",(values if values is not None else self.marks_stat()).items())
    def best_marks_plot(self):
        return self.chart("best","П’ять найкращих, балів за хвилину",[(r[0][:4],r[2]) for r in self.best_marks_per_time()])

class KmrWork(KmrCsv,Statistic,Plots):
    kmrs={}
    cat=ROOT/"results"
    def __init__(self,ref,num):
        super().__init__(ref,num)
        self.kmrs[num]=str(ref)
    @classmethod
    def compare_csv(cls,a,b):
        lines=["КМР | спроби | середній бал | середній час, хв"]
        for work in (a,b):
            lines.append(f"{work.num} | {len(work.rows)} | {mean(r.mark for r in work.rows):.2f} | {mean(r.seconds for r in work.rows)/60:.2f}")
        report="\n".join(lines)
        print(report)
        a.cat.mkdir(parents=True,exist_ok=True)
        (a.cat/"comparison.txt").write_text(report,encoding="utf8")
    @classmethod
    def compare_avg_plots(cls,a,b,show=True):
        for work in (a,b):
            path=work.avg_plot()
            if show:
                webbrowser.open(path.as_uri())

if __name__=="__main__":
    first=KmrWork(ROOT.parent/"05"/"marks.lab6.csv",1)
    second=KmrWork(ROOT/"marks2.lab11.csv",2)
    second.avg_plot()
    second.marks_plot()
    second.best_marks_plot()
    KmrWork.compare_csv(first,second)
    KmrWork.compare_avg_plots(first,second,"--no-show" not in sys.argv)
