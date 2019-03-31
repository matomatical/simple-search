"""
Analyse preprocessed documents to help me construct a list of stopwords.
"""

import pickle
from collections import Counter
# load preprocessed docs (takes about 10s)
print("LOADING...")
with open("preproc.p", "rb") as pickle_jar:
    documents = pickle.load(pickle_jar)

print("COUNTING...")
df_t = Counter()
for _, doc in documents:
    df_t.update(set(doc))

print("SCALING...")
N = len(documents)
for t in df_t:
    df_t[t] /= N

print("MOST COMMON: call top(k)")
def top(k):
    print(f"top {k}:")
    print(f"{'i':5} {'term':20s} {'frac'}\n---------------------------------")
    for i, (term, frac) in enumerate(df_t.most_common(k)):
        print(f"{i:5} {term:20s} {frac:.2%}")

# manually search list for stopwords:

"""
top 200:
i     term                 frac
---------------------------------
    0 the                  66.12%  # stop!
    1 categori             64.94%  # stop!
    2 a                    63.33%  # stop!
    3 in                   63.03%  # stop!
    4 of                   62.53%  # stop!
    5 is                   59.68%  # stop!
    6 and                  51.47%  # stop!
    7 refer                38.54%  # stop!
    8 to                   38.33%  # stop!
    9 it                   37.21%  # stop!
   10 was                  36.77%  # stop!
   11 from                 34.49%  # stop!
   12 on                   33.17%  # stop!
   13 for                  32.87%  # stop!
   14 other                30.38%  # stop!
   15 by                   28.46%  # stop!
   16 as                   28.45%  # stop!
   17 an                   27.64%  # stop!
   18 peopl                26.74%  # stop!
   19 with                 24.63%  # stop!
   20 redirect             24.60%  # stop!
   21 at                   23.62%  # stop!
   22 websit               22.57%  # stop!
   23 that                 21.34%  # stop!
   24 thumb                20.87%  # stop!
   25 are                  20.20%  # stop!
   26 birth                20.06%  # stop!
   27 he                   19.66%  # stop!
   28 also                 19.48%  # stop!
   29 live                 18.52%  # stop!
   30 has                  18.41%  # stop!
   31 or                   17.42%  # stop!
   32 be                   17.04%  # stop!
   33 this                 16.71%  # stop!
   34 one                  15.86%  # stop!
   35 born                 15.50%  # stop!
   36 which                15.31%  # stop!
   37 state                15.30%  # stop!
   38 first                14.93%
   39 they                 14.73%  # stop!
   40 his                  14.11%  # stop!
   41 new                  14.03%  # stop!
   42 unit                 13.91%
   43 have                 13.23%  # stop!
   44 use                  13.22%  # stop!
   45 american             13.04%
   46 there                12.99%  # stop!
   47 1                    12.90%
   48 name                 12.88%
   49 not                  12.88%  # stop!
   50 were                 12.58%  # stop!
   51 known                12.40%  # stop!
   52 right                12.31%  # stop!
   53 death                12.26%  # stop!
   54 year                 12.11%  # stop!
   55 after                12.05%  # stop!
   56 most                 12.00%  # stop!
   57 citi                 11.81%
   58 call                 11.77%
   59 about                11.62%  # stop!
   60 2                    11.59%
   61 time                 11.54%
   62 but                  11.53%  # stop!
   63 who                  11.10%  # stop!
   64 mani                 11.05%  # stop!
   65 when                 10.86%  # stop!
   66 two                  10.67%
   67 -                    10.63%  # stop!
   68 their                10.46%  # stop!
   69 part                 10.26%
   70 may                  10.20%  # stop!
   71 found                9.99%
   72 had                  9.89%  # stop!
   73 3                    9.78%
   74 nation               9.78%
   75 world                9.72%
   76 made                 9.67%
   77 all                  9.60%  # stop!
   78 includ               9.59%  # stop!
   79 can                  9.57%  # stop!
   80 some                 9.44%  # stop!
   81 play                 9.27%
   82 more                 8.94%  # stop!
   83 die                  8.93%  # stop!
   84 been                 8.86%  # stop!
   85 into                 8.72%  # stop!
   86 4                    8.51%
   87 relat                8.35%  # stop!
   88 work                 8.19%
   89 histori              8.04%
   90 dure                 8.00%  # stop!
   91 page                 7.94%  # stop!
   92 5                    7.73%
   93 commun               7.67%
   94 make                 7.66%
   95 offici               7.56%
   96 up                   7.48%  # stop!
   97 becaus               7.47%  # stop!
   98 franc                7.47%
   99 north                7.41%
  100 like                 7.27%  # stop!
  101 10                   7.24%
  102 start                7.19%
  103 univers              7.13%
  104 than                 7.06%  # stop!
  105 movi                 7.01%
  106 over                 7.01%  # stop!
  107 between              6.99%  # stop!
  108 these                6.93%  # stop!
  109 place                6.91%
  110 age                  6.81%
  111 2007                 6.81%
  112 6                    6.75%
  113 becam                6.71%  # stop!
  114 region               6.70%
  115 where                6.69%  # stop!
  116 veri                 6.60%
  117 area                 6.58%
  118 english              6.51%
  119 2006                 6.39%
  120 januari              6.38%
  121 three                6.36%
  122 south                6.36%
  123 2005                 6.34%
  124 2010                 6.31%
  125 such                 6.31%  # stop!
  126 countri              6.27%
  127 show                 6.22%
  128 group                6.21%
  129 2008                 6.20%
  130 later                6.17%
  131 mean                 6.17%
  132 list                 6.16%
  133 second               6.12%
  134 7                    6.11%
  135 differ               6.09%
  136 then                 6.07%  # stop!
  137 8                    6.04%
  138 no                   6.04%  # stop!
  139 player               6.02%
  140 12                   5.98%
  141 main                 5.98%
  142 former               5.96%
  143 de                   5.95%
  144 them                 5.90%  # stop!
  145 life                 5.88%
  146 out                  5.87%
  147 befor                5.87%  # stop!
  148 us                   5.85%  # stop!
  149 she                  5.83%  # stop!
  150 2009                 5.81%
  151 member               5.81%
  152 so                   5.78%  # stop!
  153 15                   5.77%
  154 march                5.77%
  155 intern               5.70%
  156 footbal              5.69%
  157 form                 5.69%
  158 20                   5.67%
  159 juli                 5.64%
  160 2004                 5.64%
  161 sinc                 5.63%  # stop!
  162 until                5.62%  # stop!
  163 television           5.59%
  164 11                   5.58%
  165 9                    5.54%
  166 left                 5.53%  # stop!
  167 career               5.48%
  168 june                 5.43%
  169 person               5.43%
  170 best                 5.42%
  171 septemb              5.42%
  172 end                  5.41%
  173 april                5.40%
  174 york                 5.37%
  175 her                  5.36%  # stop!
  176 octob                5.35%
  177 august               5.33%
  178 2001                 5.31%
  179 2000                 5.29%
  180 team                 5.28%
  181 ear                  5.28%
  182 often                5.24%  # stop!
  183 war                  5.23%
  184 gener                5.21%
  185 day                  5.20%
  186 13                   5.19%
  187 depart               5.18%
  188 30                   5.14%
  189 decemb               5.12%
  190 2003                 5.12%
  191 music                5.09%
  192 novemb               5.08%
  193 releas               5.07%
  194 famili               5.06%
  195 14                   5.05%
  196 john                 5.02%
  197 do                   5.02%  # stop!
  198 16                   5.01%
  199 number               5.01%
"""
