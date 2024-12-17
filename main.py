import flet as ft
from rembg import remove
from PIL import Image
import base64
import io
import shutil

def main(page: ft.Page):
    page.title = "Background Remover Tool"
    page.theme_mode = ft.ThemeMode.DARK  # Koyu tema
    page.bgcolor = ft.colors.BLACK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Varsayılan resim yolu
    example_image_path = "assets/images/sample.png"
    temp_file_path = "output.png"

    # Görsel placeholder'ları
    uploaded_image = ft.Image(width=300, height=300, fit=ft.ImageFit.CONTAIN, src='images/fox.jpg')
    result_image = ft.Image(width=300, height=300, fit=ft.ImageFit.CONTAIN, src='images/output.png')

    # Kaydedilecek dosya yolu için FilePicker
    save_file_picker = ft.FilePicker(on_result=lambda e: save_result(e))
    page.overlay.append(save_file_picker)

    # Resim işleme fonksiyonu
    def process_image(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            with open(file_path, "rb") as f:
                input_data = f.read()

            # Arka plan kaldırma işlemi
            output_data = remove(input_data)

            # Base64 formatına dönüştür
            base64_data = base64.b64encode(output_data).decode("utf-8")

            # Çıktıyı geçici bir dosyaya kaydet
            with open(temp_file_path, "wb") as f:
                f.write(output_data)

            # Görselleri güncelle
            uploaded_image.src = file_path
            result_image.src_base64 = base64_data
            page.update()

    # Dosya kaydetme fonksiyonu
    def save_result(e: ft.FilePickerResultEvent):
        if e.path:
            # Geçici dosyayı seçilen konuma kopyala
            shutil.copy(temp_file_path, e.path)
            print(f"File saved to {e.path}")
            page.snack_bar = ft.SnackBar(ft.Text("File saved successfully!"), open=True)
            page.update()

    # Dosya seçici
    file_picker = ft.FilePicker(on_result=process_image)
    page.overlay.append(file_picker)

    # Kart tasarımları
    upload_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Upload an Image", size=18, weight="bold", color=ft.colors.WHITE),
                    ft.ElevatedButton(
                        "Choose Image",
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=lambda _: file_picker.pick_files(),
                        bgcolor=ft.colors.BLUE_800,
                        color=ft.colors.WHITE,
                    ),
                    ft.Text("Supported formats: PNG, JPG, JPEG", size=12, color=ft.colors.GREY_400),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=20,
            alignment=ft.alignment.center,
        ),
        elevation=10,
    )

    result_card = ft.Card(
        content=ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Original Image", weight="bold", color=ft.colors.WHITE),
                            uploaded_image,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    ft.Column(
                        [
                            ft.Text("Background Removed", weight="bold", color=ft.colors.WHITE),
                            result_image,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=20,
        ),
        elevation=10,
    )

    download_button = ft.ElevatedButton(
        "Save Result",
        icon=ft.icons.DOWNLOAD,
        on_click=lambda _: save_file_picker.save_file(
            dialog_title="Save Image",
            file_name="output.png",  # Kaydetme penceresine önerilen varsayılan isim
            allowed_extensions=["png"],
            file_type=ft.FilePickerFileType.CUSTOM,
        ),
        bgcolor=ft.colors.GREEN_800,
        color=ft.colors.WHITE,
    )

    # Ana düzen
    page.add(
        ft.Column(
            [
                ft.Text("Background Remover Tool", size=24, weight="bold", color=ft.colors.WHITE),
                upload_card,
                result_card,
                download_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
        )
    )

ft.app(target=main, assets_dir='assets')
