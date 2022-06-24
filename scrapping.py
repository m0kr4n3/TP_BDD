from requests import get
from bs4 import BeautifulSoup
import json, re



headers = {
    "Cookie": '_csrf=44271cf543b002d09d0c6e35cfeba868869c2ae10faf37ec24056af46edbfa64a:2:{i:0;s:5:"_csrf";i:1;s:32:"D9yU7midx51lHX2aaPjXBEHORCdzcmsm";}; _ga=GA1.2.239957291.1656075417; _gid=GA1.2.1470275687.1656075417; _gat=1',
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
}


def get_rencontres_sans_resultat(journee, group):
    url = f"https://lfwa.dz/programme/print?id={str(journee)}&div=1&cat=1&grp={str(24+group)}"
    r = get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")
    table = soup.find("table")

    column_names = [
        column.text for column in table.findChildren("thead")[0].findChildren("th")
    ]
    rencontres = []

    for tr in table.findAll("tr")[2:]:
        rencontre = {}
        data = tr.findChildren()
        for i in range(len(column_names)):
            rencontre[column_names[i]] = data[i].text
        # print(rencontre)
        rencontres.append(rencontre)
    return rencontres


def get_resultat_du_group(g):
    group = {"journees": []}
    for num_journee in range(1, 27):
        journee = {"num": num_journee}

        journee["rencontres"] = get_rencontres_sans_resultat(num_journee, g)

        rencontres_avec_resultat = attribute_results_to_rencontres(num_journee, 1)
        for rencontre in rencontres_avec_resultat:
            non_trouv = True
            for ind, ren_s in enumerate(journee["rencontres"]):
                # print(f"{rencontre['rencontre']}    {ren_s['Rencontre']}");input()
                if rencontre["rencontre"] == ren_s["Rencontre"]:
                    non_trouv = False
                    ren_s["buts"] = rencontre["buts"]
                    ren_s["score"] = rencontre["score"]
                    journee["rencontres"][ind] = ren_s
                    break
            if non_trouv:
                print("rencontre non trouvee!!!")
                exit()

        # print(journee);input()
        group["journees"].append(journee)
    return group


def attribute_results_to_rencontres(journee, group):
    url = (
        f"http://lfwa.dz/programme/journee?id={str(journee)}&cat=1&grp={str(24+group)}"
    )
    r = get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")
    links = [
        f"http://lfwa.dz{link.attrs['href']}"
        for link in soup.findAll("a", attrs={"class": "btn theme"})
    ]
    rencontres = []
    for link in links:
        rencontres.append(attribute_result_to_rencontre(link))
    return rencontres


def attribute_result_to_rencontre(link):
    r = get(link, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")
    rencontre = "{} - {}".format(
        *[i.text for i in soup.findAll("span", attrs={"class": "d-none d-sm-block"})]
    )
    score = soup.find("div", attrs={"class": "result-match"}).text.strip()
    equipeA = soup.find("div", attrs={"class": "team"})
    equipeA_name = equipeA.find("span").text
    buts = []
    b = equipeA.find("ul").findAll("li")
    if b != []:
        for i in b:

            i = i.text.strip().replace("'", "").replace("+", "").split(" ")
            but = {"equipe": equipeA_name, "joueur": " ".join(i[:-1]), "minute": i[-1]}
            buts.append(but)

    equipeB = soup.find("div", attrs={"class": "team right"})
    equipeB_name = equipeB.find("span").text
    b = equipeB.find("ul").findAll("li")
    if b != []:
        for i in b:
            i = i.text.strip().replace("'", "").replace("+", "").split(" ")
            but = {"equipe": equipeB_name, "joueur": " ".join(i[:-1]), "minute": i[-1]}
            buts.append(but)
    rencontre = {"rencontre": rencontre, "score": score, "buts": buts}
    return rencontre


def get_clubs_infos(group):
    url = f"http://lfwa.dz/programme/journee?id=1&cat=1&grp={str(24+group)}"
    r = get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")
    links = [
        l.attrs["href"]
        for l in soup.findAll("a")
        if re.search("^/club/view", l.attrs["href"]) != None
    ]

    clubs = []
    for link in links:
        club = get_club_info(link)
        if club is not None:
            clubs.append(club)
    return clubs


def get_club_info(link):
    r = get(f"http://lfwa.dz{link}", headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")
    club = {"equipe": soup.find("h1").text.split("(")[1].split(")")[0]}
    if club["equipe"] == "#8":
        return None
    infos = soup.find("ul", attrs={"class": "general-info"}).findAll("li")
    for info in infos:
        info = info.text.split(":")
        club[info[0].strip()] = info[1].strip()
    club["joueurs"]=[]
    joueurs=[info.find('h4').text.strip() for info in soup.find('div',attrs={'id': "players"}).findAll('div',attrs={'class': "info-player"})]
    for j in joueurs:
        j=j.split('   ')
        joueur = {
            "nom":j[0].strip(),
            "poste": j[-1].strip()
        }
        club["joueurs"].append(joueur)

    # print(club)
    return club


if __name__ == "__main__":

    # Retrivieving Rencontres
    # group = get_resultat_du_group(1)

    # with open('rencontres.json','w',encoding='utf8') as w:
    #     json.dump(group, w, indent=4,ensure_ascii=False)




    # Retrieving Buts
    clubs = get_clubs_infos(1)

    with open("clubs.json", "w", encoding="utf8") as w:
        json.dump(clubs, w, indent=4, ensure_ascii=False)
    # Faudrait rajouter les 2 clubs CROF et CRDB manuellement car leurs liens ne fonctionnent pas
