"""
HOX HOX
Ainoa tehtävä on luoda config.json tiedosto uudelleen
mikäeli sen satut poistamaan.
"""
import json

confit = {
    "luo_valikko": {
        
        "otsikko": {
            "bg": "grey",
            "fg": "black",
            "text": "Miinaharava",
            "width": "500",
            "height": "2",
            "font": "bold"
        },
        
        "painike": {
            "bg": "grey",
            "text": "Aloita peli", 
            "width": "30",
            "height": "2",
            "font": "bold"
        },
    },
    "lopetus_valikko": {
        "painike1": {
            "bg": "grey",
            "text": "Uusi peli", 
            "width": "30",
            "height": "2",
            "font": "bold"
        },
        "painike2": {
            "bg": "grey",
            "text": "Lopeta peli",
            "width": "10",
            "height": "1",
            "font": "bold"
        },
        
        "kysymys_teksti": {
            "text": "Haluatko pelata uudelleen?",
            "font": "bold"
        }
    }
}
def luo_config():
    with open("config.json", "w") as config:
        json.dump(confit, config, sort_keys=True, indent=4)

luo_config()
