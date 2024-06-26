import pygame
import random
from PIL import Image

class QuickSortVisualization:
    def __init__(self, arr):
        pygame.init()  # Initialize all imported pygame modules
        self.arr = arr
        self.size = len(arr)
        self.window_width = 800
        self.window_height = 600
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Quick Sort Visualization")
        self.clock = pygame.time.Clock()
        self.colors = [(255, 255, 255) for _ in range(self.size)]  # Initial color for each bar
        self.bar_width = self.window_width // self.size
        self.max_height = max(self.arr)
        self.done = False
        self.paused = False
        self.record = True
        self.frames = []
        self.speed = 50  # Initial speed
        self.sorting = False

    def quick_sort(self, low, high):
        if low < high:
            pi = self.partition(low, high)

            # Recursively sort elements before and after partition
            self.quick_sort(low, pi - 1)
            self.quick_sort(pi + 1, high)

    def partition(self, low, high):
        pivot = self.arr[high]
        i = low - 1
        for j in range(low, high):
            if self.arr[j] < pivot:
                i += 1
                self.arr[i], self.arr[j] = self.arr[j], self.arr[i]

                # Redraw the bars with different colors after each swap
                self.colors = [(0, 255, 0) if k == i or k == j else (255, 255, 255) for k in range(self.size)]
                self.draw_bars(f"Swapping: {self.arr[i]} and {self.arr[j]}")
                self.frames.append(pygame.surfarray.array3d(self.screen))  # Record frame
                pygame.display.update()  # Update display after drawing bars
                self.clock.tick(self.speed)  # Adjust the frame rate

        self.arr[i + 1], self.arr[high] = self.arr[high], self.arr[i + 1]

        return i + 1

    def draw_bars(self, status=""):
        self.screen.fill((50, 50, 50))  # Clear the screen with a background color
        font = pygame.font.Font(None, 24)  # Font for displaying text

        for i, (height, color) in enumerate(zip(self.arr, self.colors)):
            normalized_height = height / self.max_height * self.window_height
            bar_rect = pygame.Rect(i * self.bar_width, self.window_height - normalized_height, self.bar_width, normalized_height)
            pygame.draw.rect(self.screen, color, bar_rect)

        # Display sorting status
        status_text = font.render(status, True, (255, 255, 255))
        self.screen.blit(status_text, (10, 10))

        pygame.display.update()  # Update display after drawing bars

    def visualize(self):
        self.sorting = True
        self.quick_sort(0, self.size - 1)
        self.colors = [(0, 255, 0) for _ in range(self.size)]  # Set the color for sorted bars
        self.draw_bars("Sorting Completed")
        if self.record:
            self.save_gif()

        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused  # Pause or resume on spacebar press
                    elif event.key == pygame.K_UP:
                        self.speed = min(300, self.speed + 10)  # Increase speed
                    elif event.key == pygame.K_DOWN:
                        self.speed = max(10, self.speed - 10)  # Decrease speed

            if self.record:
                self.save_gif()

        pygame.quit()

    def save_gif(self):
        try:
            pil_images = [Image.fromarray(frame.swapaxes(0, 1)) for frame in self.frames]  # Convert to PIL Images
            pil_images[0].save('quick_sort_simulation.gif', save_all=True, append_images=pil_images[1:], loop=0, duration=1000//30)  # Save as GIF
            print("GIF saved successfully!")
        except Exception as e:
            print(f"Error saving GIF: {e}")

# Usage
arr = random.sample(range(1, 101), 100)  # Generate 100 unique random integers between 1 and 100
sort_viz = QuickSortVisualization(arr)
sort_viz.visualize()
