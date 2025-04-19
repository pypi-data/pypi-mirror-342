from richtqdm import RichTqdm
import time


def test_rich_tqdm():
    """
    Test the RichTqdm class.
    """
    # Create a RichTqdm instance
    with RichTqdm(total=100) as pbar:
        for i in range(100):
            pbar.update(1)
            pbar.set_description(f"Processing {i}")

            time.sleep(0.1)


if __name__ == "__main__":
    test_rich_tqdm()
    print("Test passed!")
