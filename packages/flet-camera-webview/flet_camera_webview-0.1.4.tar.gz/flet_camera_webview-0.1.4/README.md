# flet_camera

📸 Кастомный компонент камеры для Flet с WebView + WebSocket.

## Установка

```
pip install flet-camera-webview
```

## Использование

```python
import flet as ft
from flet_camera import CameraWebView


def main(page):
    cam = CameraWebView(page)
    
    def save(e):
        image = cam.get_image_bytes()
        if image:
            with open("photo.jpg", "wb") as f:
                f.write(image)

    page.add(
        ft.Column(
            [
                ft.Stack(
                    [
                        ft.Container(
                            content=cam,
                            border_radius=150,  # 🎯 закругление — круг!
                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.BLACK
                        )
                    ],
                    width=300,
                    height=300,
                    expand=False
                ),
                ft.ElevatedButton(
                    "📸 Снимок",
                    on_click=save,
                    width=160,
                    height=48,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=25),
                        padding=20
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )



ft.app(target=main, view=ft.WEB_BROWSER)
```
