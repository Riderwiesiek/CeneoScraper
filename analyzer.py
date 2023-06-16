import os
import json
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


#print(*[filename.removesuffix(".json") for filename in os.listdir()], sep="\n")
print(*list(map(lambda x: x.removesuffix(".json"), os.listdir("opinions"))), sep="\n")
product_code = input("Podaj kod produktu: ")
opinions = pd.read_json(f"opinions/{product_code}.json")
opinions.stars = opinions.stars.map(lambda x: float(x.split("/")[0].replace(",",".")))
stats ={
    #'opinions_count': len(opinions),
    'opinions_count': opinions.shape[0],
    'pros_count': opinions.pros.map(bool).sum(),
    'cons_count': opinions.cons.map(bool).sum(),
    'average_score': opinions.stars.mean()
}
print(f"""Dla produktu o identyfikatorze {product_code}
pobrano {stats["opinions_count"]} opinii.
Dla {stats["pros_count"]} opinii podana została lista zalet produktu, 
a dla {stats["cons_count"]} opinii podana została lista jego wad.
Średnia ocena produktu wynosi{stats["average_score"]:.2f}.""")
colors_stars ={}
for i in np.arange(0,5.5,0.5):
    colors_stars[i] = "crimson" if i <= 2.5 else "steelblue" if i <= 3.5 else "forestgreen"
stars = opinions.stars.value_counts().sort_index().reindex(list(np.arange(0,5.5,0.5)), fill_value=0)
print(stars)
stars.plot.bar(color=["crimson","crimson","crimson","crimson","crimson","crimson","steelblue","steelblue","forestgreen","forestgreen","forestgreen",])
plt.xticks(rotation='horizontal')
plt.title("Rozkład liczby gwiazdek w opiniach konsumentów")
plt.xlabel("Liczba gwiazdek")
plt.xlabel("liczba opini")
plt.ylim(0,max(stars)+10)
for index, value in enumerate(stars):
    plt.text(index, value+0.5, str(value), ha = "center")
plt.savefig(f"charts/{product_code}_stars.png")
plt.close()


recomendation = opinions["recomendation"].value_counts(dropna = False). reindex(["Polecam","Nie polecam", None], fill_value=0)
print(recomendation)
recomendation.plot.pie(
    label="",
    autopct= lambda p: '{:.1f}%' .format(round(p)) if p > 0 else '',
    labels = ["Polecam", "Nie polecam", "Nie mam zdania"],
    colors = ["forestgreen", "crimson", "teelblue"]
)
plt.legend(loc='upper center', ncol=3)
plt.title("Rozkład rekomendacji w opiniach konsumentów")
plt.savefig(f"./charts/{product_code}_recomendation.png")
plt.close()

#stats['stars'] = stars.to_dict()
#stats['recomendation'] = recomendation.to_dict()

#with open(f"ststs/{product_code}.json", "w", encoding="UTF-8") as jf:
#    json.dump(stats, jf, indent=4, ensure_ascii=False)