from pathlib import Path
from dataclasses import dataclass

@dataclass
class PathConstants: 
    constant_file_path: Path = Path(__file__)
    project_base_path: Path = constant_file_path.parents[2]
    database_path: Path = project_base_path.joinpath("data/database.sqlite")
    configs_path: Path = project_base_path.joinpath("configs")

@dataclass
class UtilityConstants:
    secondary_columns = [
        "Batı",
        "Doğu",
        "Güney",
        "Kuzey",
        "ADSL",
        "Ahşap Doğrama",
        "Akıllı Ev",
        "Alarm (Hırsız)",
        "Alarm (Yangın)",
        "Alaturka Tuvalet",
        "Alüminyum Doğrama",
        "Amerikan Kapı",
        "Amerikan Mutfak",
        "Ankastre Fırın",
        "Asansör",
        "Barbekü",
        "Beyaz Eşya",
        "Boyalı",
        "Bulaşık Makinesi",
        "Buzdolabı",
        "Çamaşır Kurutma Makinesi",
        "Çamaşır Makinesi",
        "Çamaşır Odası",
        "Çelik Kapı",
        "Duşakabin",
        "Duvar Kağıdı",
        "Ebeveyn Banyosu",
        "Fırın",
        "Fiber İnternet",
        "Giyinme Odası",
        "Gömme Dolap",
        "Görüntülü Diafon",
        "Hilton Banyo",
        "Intercom Sistemi",
        "Isıcam",
        "Jakuzi",
        "Kartonpiyer",
        "Kiler",
        "Klima",
        "Küvet",
        "Laminat Zemin",
        "Marley",
        "Mobilya",
        "Mutfak (Ankastre)",
        "Mutfak (Laminat)",
        "Mutfak Doğalgazı",
        "Panjur/Jaluzi",
        "Parke Zemin",
        "PVC Doğrama",
        "Seramik Zemin",
        "Set Üstü Ocak",
        "Spot Aydınlatma",
        "Şofben",
        "Şömine",
        "Teras",
        "Termosifon",
        "Vestiyer",
        "Wi-Fi",
        "Yüz Tanıma & Parmak İzi",
        "24 Saat Güvenlik",
        "Buhar Odası",
        "Çocuk Oyun Parkı",
        "Hamam",
        "Hidrofor",
        "Isı Yalıtımı",
        "Jeneratör",
        "Kablo TV",
        "Kamera Sistemi",
        "Kapıcı",
        "Kreş",
        "Müstakil Havuzlu",
        "Otopark - Açık",
        "Otopark - Kapalı",
        "Sauna",
        "Ses Yalıtımı",
        "Siding",
        "Spor Alanı",
        "Su Deposu",
        "Tenis Kortu",
        "Uydu",
        "Yangın Merdiveni",
        "Yüzme Havuzu (Açık)",
        "Yüzme Havuzu (Kapalı)",
        "Alışveriş Merkezi",
        "Belediye",
        "Cami",
        "Cemevi",
        "Denize Sıfır",
        "Eczane",
        "Eğlence Merkezi",
        "Fuar",
        "Hastane",
        "Havra",
        "İlkokul-Ortaokul",
        "İtfaiye",
        "Kilise",
        "Lise",
        "Market",
        "Park",
        "Plaj",
        "Polis Merkezi",
        "Sağlık Ocağı",
        "Semt Pazarı",
        "Spor Salonu",
        "Şehir Merkezi",
        "Üniversite",
        "Anayol",
        "Avrasya Tüneli",
        "Boğaz Köprüleri",
        "Cadde",
        "Deniz Otobüsü",
        "Dolmuş",
        "E-5",
        "Havaalanı",
        "İskele",
        "Marmaray",
        "Metro",
        "Metrobüs",
        "Minibüs",
        "Otobüs Durağı",
        "Sahil",
        "Teleferik",
        "TEM",
        "Tramvay",
        "Tren İstasyonu",
        "Troleybüs",
        "Boğaz",
        "Deniz",
        "Doğa",
        "Göl",
        "Havuz",
        "Park & Yeşil Alan",
        "Şehir",
        "Ara Kat",
        "Ara Kat Dubleks",
        "Bahçe Dubleksi",
        "Bahçe Katı",
        "Bahçeli",
        "Çatı Dubleksi",
        "En Üst Kat",
        "Forleks",
        "Garaj / Dükkan Üstü",
        "Giriş Katı",
        "Kat Dubleksi",
        "Loft",
        "Müstakil Girişli",
        "Ters Dubleks",
        "Tripleks",
        "Zemin Kat",
        "Araç Park Yeri",
        "Banyo",
        "Geniş Koridor",
        "Giriş / Rampa",
        "Merdiven",
        "Mutfak",
        "Oda Kapısı",
        "Priz / Elektrik Anahtarı",
        "Tutamak / Korkuluk",
        "Tuvalet",
        "Yüzme Havuzu"
    ]