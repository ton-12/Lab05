import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"


def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # Abilita lo scorrimento verticale sulla pagina principale
    page.scroll = ft.ScrollMode.AUTO

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    lista_strumenti = ft.ListView(height=300, spacing=5, padding=10, auto_scroll=True)

    # --- SEZIONE 3: Tutti i TextField per il nuovo strumento ---
    input_tipo = ft.TextField(label="Tipo strumento", hint_text="Es. Chitarra")
    input_marca = ft.TextField(label="Marca", hint_text="Es. Fender")
    input_anno = ft.TextField(label="Anno di acquisto", hint_text="Es. 2023")

    # Contatore per il valore in Euro (inizializzato a 100)
    txt_valore = ft.Text(value="100", size=20, weight=ft.FontWeight.BOLD)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    # Handlers per incrementare/decrementare il valore in euro dello strumento
    def riduci_valore(e):
        valore_attuale = int(txt_valore.value)
        if valore_attuale > 0:
            txt_valore.value = str(valore_attuale - 10)  # Decrementa di 1€ alla volta
            page.update()

    def aumenta_valore(e):
        valore_attuale = int(txt_valore.value)
        txt_valore.value = str(valore_attuale + 10)  # Incrementa di 1€ alla volta
        page.update()

    # Handler per aggiungere lo strumento con validazione dei dati numerici
    def aggiungi_nuovo_strumento(e):
        tipo = input_tipo.value.strip()
        marca = input_marca.value.strip()
        anno_str = input_anno.value.strip()
        valore = float(txt_valore.value)

        if not tipo or not marca or not anno_str:
            alert.show_alert("Tutti i campi (Tipo, Marca, Anno) devono essere compilati.")
            return

        try:
            anno = int(anno_str)
        except ValueError:
            alert.show_alert("L'anno di acquisto inserito non è valido. Inserire un valore numerico intero.")
            return

        try:
            deposito.aggiungi_strumento(tipo, marca, anno, valore)

            input_tipo.value = ""
            input_marca.value = ""
            input_anno.value = ""
            txt_valore.value = "100"

            aggiorna_lista_strumenti()

        except Exception as errore_deposito:
            alert.show_alert(f"Errore durante l'inserimento: {errore_deposito}")

    # --- EVENTI / PULSANTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    btn_meno = ft.IconButton(icon=ft.Icons.REMOVE, on_click=riduci_valore)
    btn_piu = ft.IconButton(icon=ft.Icons.ADD, on_click=aumenta_valore)
    pulsante_aggiungi_strumento = ft.Button("Aggiungi strumento", on_click=aggiungi_nuovo_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20, weight=ft.FontWeight.BOLD),
        ft.Row(
            spacing=20,
            controls=[input_responsabile, pulsante_conferma_responsabile],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Divider(),

        # Sezione 3
        ft.Text("Aggiungi Nuovo Strumento", size=20, weight=ft.FontWeight.BOLD),
        ft.Column(
            controls=[
                input_tipo,
                input_marca,
                input_anno,
                ft.Row(
                    controls=[
                        ft.Text("Valore (€): ", size=16),
                        btn_meno,
                        txt_valore,
                        btn_piu
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                pulsante_aggiungi_strumento
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20, weight=ft.FontWeight.BOLD),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()


ft.run(main)
