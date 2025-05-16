import requests
import pandas as pd
import matplotlib.pyplot as plt

CONFIG_TARGET_URL = "https://eci.ec.europa.eu/043/public/api/report/map"
CONFIG_SAVE_FILE = "output/data.csv"
CONFIG_CHART_IMAGE_FILE = "output/chart.png"


def fetch_data() -> None:
    response = requests.get(
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        url=CONFIG_TARGET_URL,
    )
    data = response.json()

    # Convertir les données en DataFrame pandas
    df = pd.DataFrame(data)

    # Aplatir le DataFrame
    flattened_df = pd.json_normalize(df["signatureCountryCount"])

    # Ajouter la colonne lastUpdate au DataFrame aplati
    flattened_df["lastUpdate"] = df["lastUpdate"]

    # Réorganiser les colonnes si nécessaire
    df = flattened_df[
        ["lastUpdate"] + [col for col in flattened_df.columns if col != "lastUpdate"]
    ]

    # index
    df = df.set_index("countryId")
    print(df)

    # Enregistrer les données dans un fichier CSV
    df.to_csv(CONFIG_SAVE_FILE)

    # Générer un graphique
    # Trier le DataFrame par ordre décroissant de percentage
    df_sorted = df.sort_values(by="percentage", ascending=False)

    # Créer le graphique
    plt.figure(figsize=(12, 8))
    colors = [
        "green" if percentage > 100.0 else "blue"
        for percentage in df_sorted["percentage"]
    ]
    bars = plt.bar(df_sorted["countryCode"], df_sorted["percentage"], color=colors)

    # Ajouter les valeurs sur les colonnes
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height:.2f}",
            ha="center",
            va="bottom",
        )

    # Ajouter des labels et un titre
    plt.xlabel("Country Code")
    plt.ylabel("Percentage")
    plt.title(f"Percentage by Country Code at {df['lastUpdate'].max()}")

    plt.savefig(CONFIG_CHART_IMAGE_FILE)


if __name__ == "__main__":
    fetch_data()
