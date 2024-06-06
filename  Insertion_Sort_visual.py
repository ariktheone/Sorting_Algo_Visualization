import pygame
import random
from PIL import Image

class InsertionSortVisualization:
    def __init__(self, arr):
        pygame.init()  # Initialize all imported pygame modules
        self.arr = arr
        self.size = len(arr)
        self.window_width = 800
        self.window_height = 600
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Insertion Sort Visualization")
        self.clock = pygame.time.Clock()
        self.colors = [(255, 255, 255) for _ in range(self.size)]  # Initial color for each bar
        self.bar_width = self.window_width // self.size
        self.max_height = max(self.arr)
        self.done = False
        self.paused = False
        self.record = True  # Automatically start recording
        self.frames = []
        self.speed = 50  # Initial speed
        self.sorting = False

    def insertion_sort_step(self):
        for i in range(1, len(self.arr)):
            key = self.arr[i]
            j = i - 1
            while j >= 0 and key < self.arr[j]:
                self.arr[j + 1] = self.arr[j]
                j -= 1
            self.arr[j + 1] = key
            
            # Redraw the bars with different colors after each swap
            self.colors = [(0, 255, 0) if k <= i else (77, 77, 255) if k == j + 1 else (255, 255, 255) for k in range(self.size)]
            self.draw_bars(f"Inserting: {key}")
            if self.record:
                self.frames.append(pygame.surfarray.array3d(self.screen))  # Record frame
            pygame.display.update()  # Update display after drawing bars
            self.clock.tick(self.speed)  # Adjust the frame rate

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
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            if self.sorting and not self.paused:
                self.insertion_sort_step()  # Perform one step of insertion sort
                if self.arr == sorted(self.arr):
                    self.sorting = False  # Stop sorting if array is sorted

            self.colors = [(0, 255, 0) if k == self.size - 1 else (255, 255, 255) for k in range(self.size)]  # Set the color for sorted bars
            self.draw_bars("Sorting Completed" if not self.sorting else "")  # Draw the bars in the final state

        if self.record:
            self.save_gif()

        pygame.quit()

    def save_gif(self):
        pil_images = [Image.fromarray(frame.swapaxes(0, 1)) for frame in self.frames]  # Convert to PIL Images
        pil_images[0].save('insertion_sort_simulation.gif', save_all=True, append_images=pil_images[1:], loop=0, duration=1000//30)  # Save as GIF
        print("GIF saved successfully!")

# Usage
arr = random.sample(range(1, 101), 100)  # Generate 100 unique random integers between 1 and 100
sort_viz = InsertionSortVisualization(arr)
sort_viz.visualize()
