import requests

class ImgAPI:
    @staticmethod
    def generate_image(prompt: str, width=1024, height=1024) -> bytes | None:
        """Генерирует изображение и возвращает его в виде байтов (bytes)."""
        formatted_prompt = requests.utils.quote(prompt)
        url = f"https://image.pollinations.ai/image/{formatted_prompt}?width={width}&height={height}&nologo=true"

        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return response.content
            else:
                print(
                    f"Ошибка сервера Pollinations: статус {response.status_code}"
                )
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка сети: {e}")
            return None

if __name__ == "__main__":
    api = ImgAPI()
    img_data = api.generate_image("big field")

    if img_data:
        with open("test.jpg", "wb") as f:
            f.write(img_data)
        print("Тестовая картинка успешно сохранена как test.jpg!")