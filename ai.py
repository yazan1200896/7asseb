import os
from typing import List


# Mockup of InferenceHTTPClient (replace with actual implementation or import)
class InferenceHTTPClient:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def infer(self, image_path: str, model_id: str):
        # Replace this block with the actual API call logic
        return {
            "image": image_path,
            "model_id": model_id,
            "result": f"Simulated result for {image_path}"
        }


class AI:
    def __init__(self, frames_dir: str, client: InferenceHTTPClient):
        self.frames_dir = frames_dir
        self.client = client

    def get_all_images(self) -> List[str]:
        """
        Retrieve all images in the frames directory.
        """
        if not os.path.exists(self.frames_dir):
            raise FileNotFoundError(f"The directory {self.frames_dir} does not exist.")

        images = [
            os.path.join(self.frames_dir, file)
            for file in os.listdir(self.frames_dir)
            if file.endswith(('.jpg', '.png', '.jpeg'))
        ]
        return images

    def infer_images(self, model_id: str) -> dict:
        """
        Infer all images and calculate total value for each based on predictions.
        """
        # Get all images in the frames directory
        images = self.get_all_images()
        image_values = []

        for image_path in images:
            result = self.client.infer(image_path, model_id)
            predictions = result.get("predictions", [])

            # Debugging logs
            print(f"Processing image: {image_path}, Predictions: {predictions}")

            total_value = 0
            detected_classes = set()  # To handle duplicates

            for prediction in predictions:
                coin_class = prediction.get("class", "")
                confidence = prediction.get("confidence", 0)

                # Define coin values
                if coin_class == "1-dinar":
                    coin_value = 1
                elif coin_class == "20-dinar":
                    coin_value = 20
                elif coin_class == "5-Piastres":
                    coin_value = 0.10
                elif coin_class == "10-Piastres":
                    coin_value = 0.10
                elif coin_class == "20-dinar":
                    coin_value = 20
                elif coin_class == "50-dinar":
                    coin_value = 50
                elif coin_class == "10-dinar":
                    coin_value = 10
                elif coin_class == "1-2-dinar":
                    coin_value = 0.5
                elif coin_class == "1-4-dinar":
                    coin_value = 0.25
                elif coin_class == "5-dinar":
                    coin_value = 5

                else:
                    coin_value = 0  # Default for unknown classes

                # Only include predictions with confidence >= 0.75
                if confidence >= 0.5 and coin_class not in detected_classes:
                    detected_classes.add(coin_class)  # Avoid duplicates
                    total_value += coin_value

                    # Debugging calculation
                    print(
                        f"Class: {coin_class}, Confidence: {confidence}, Coin Value: {coin_value}, Running Total: {total_value}")
                else:
                    # Debugging skipped predictions
                    print(f"Skipped prediction: Class: {coin_class}, Confidence: {confidence}")

            print(f"Total Value for {image_path}: {total_value}")
            image_values.append((image_path, total_value))

            # Delete processed image
            try:
                os.remove(image_path)
            except OSError as e:
                print(f"Error deleting file {image_path}: {e}")

        # Sort images by total value
        image_values.sort(key=lambda x: x[1], reverse=True)
        best_image = image_values[0][0] if image_values else None
        best_value = image_values[0][1] if image_values else 0

        return {"best_image": best_image, "total_value": best_value}
