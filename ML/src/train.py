import os
import json
import numpy as np
from deepface import DeepFace


class FaceTrainer:
    """Handles training the face recognition model using saved face images."""

    def __init__(self, dataset_dir: str = "datasets", model_dir: str = "models",
                 model_name: str = "VGG-Face"):
        self.dataset_dir = dataset_dir
        self.model_dir = model_dir
        self.model_name = model_name
        self.encodings = {}

    def _setup_model_dir(self):
        """Create models directory if it doesn't exist."""
        os.makedirs(self.model_dir, exist_ok=True)

    def _get_students(self) -> list:
        """Return list of student IDs from dataset directory."""
        if not os.path.exists(self.dataset_dir):
            raise FileNotFoundError(f"Dataset directory '{self.dataset_dir}' not found.")
        return [
            s for s in os.listdir(self.dataset_dir)
            if os.path.isdir(os.path.join(self.dataset_dir, s))
        ]

    def _get_images(self, student_id: str) -> list:
        """Return list of image paths for a given student."""
        student_folder = os.path.join(self.dataset_dir, student_id)
        return [
            os.path.join(student_folder, img)
            for img in os.listdir(student_folder)
            if img.endswith((".jpg", ".jpeg", ".png"))
        ]

    def _generate_embedding(self, img_path: str) -> list | None:
        """Generate face embedding for a single image."""
        try:
            result = DeepFace.represent(
                img_path=img_path,
                model_name=self.model_name,
                enforce_detection=False
            )
            return result[0]["embedding"]
        except Exception as e:
            print(f"[WARNING] Skipped {img_path}: {e}")
            return None

    def _process_student(self, student_id: str):
        """Generate and store average embedding for a student."""
        images = self._get_images(student_id)

        if not images:
            print(f"[WARNING] No images found for student: {student_id}")
            return

        print(f"[INFO] Processing student: {student_id} ({len(images)} images)")

        embeddings = []
        for img_path in images:
            embedding = self._generate_embedding(img_path)
            if embedding:
                embeddings.append(embedding)
                print(f"  [✓] {os.path.basename(img_path)}")

        if embeddings:
            # Average all embeddings into one representative vector
            avg_embedding = np.mean(embeddings, axis=0).tolist()
            self.encodings[student_id] = avg_embedding
            print(f"[INFO] Saved embedding for student: {student_id}")
        else:
            print(f"[ERROR] No valid embeddings for student: {student_id}")

    def _save_encodings(self):
        """Save all encodings to a JSON file."""
        output_path = os.path.join(self.model_dir, "encodings.json")
        with open(output_path, "w") as f:
            json.dump(self.encodings, f)
        print(f"\n[INFO] Encodings saved to '{output_path}'")

    def train(self):
        """Main method to train the face recognition model."""
        self._setup_model_dir()

        students = self._get_students()

        if not students:
            print("[ERROR] No students found in dataset. Run capture_face.py first.")
            return

        print(f"[INFO] Found {len(students)} student(s). Starting training...\n")

        for student_id in students:
            self._process_student(student_id)

        self._save_encodings()
        print(f"[INFO] Training complete! {len(self.encodings)} student(s) encoded.")


if __name__ == "__main__":
    trainer = FaceTrainer()
    trainer.train()
