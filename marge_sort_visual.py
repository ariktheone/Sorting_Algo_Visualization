import pygame
import random

class MergeSortVisualization:
    def __init__(self, arr):
        pygame.init()  # Initialize all imported pygame modules
        self.arr = arr
        self.size = len(arr)
        self.window_width = 800
        self.window_height = 600
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Merge Sort Visualization")
        self.clock = pygame.time.Clock()
        self.done = False
        self.paused = False
        self.record = False
        self.frames = []
        self.speed = 0.00000001  # Initial speed
        self.sorting = False

    def merge(self, left, right):
        merged = []
        while left and right:
            if left[0] < right[0]:
                merged.append(left.pop(0))
            else:
                merged.append(right.pop(0))
        merged.extend(left)
        merged.extend(right)
        return merged

    def merge_sort(self, arr):
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        left = self.merge_sort(left)
        right = self.merge_sort(right)

        return self.merge(left, right)

    def draw_bars(self, status=""):
        self.screen.fill((50, 50, 50))  # Clear the screen with a background color
        font = pygame.font.Font(None, 24)  # Font for displaying text

        max_height = max(self.arr)
        for i, height in enumerate(self.arr):
            bar_rect = pygame.Rect(i * (self.window_width // self.size), self.window_height - height * 5, self.window_width // self.size, height * 5)
            pygame.draw.rect(self.screen, (255, 255, 255), bar_rect)

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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused  # Pause or resume on spacebar press
                    elif event.key == pygame.K_r:
                        self.record = True  # Start recording on 'r' press
                    elif event.key == pygame.K_UP:
                        self.speed = min(300, self.speed + 10)  # Increase speed
                    elif event.key == pygame.K_DOWN:
                        self.speed = max(10, self.speed - 10)  # Decrease speed

            if self.sorting and not self.paused:
                self.arr = self.merge_sort(self.arr)  # Perform merge sort
                self.sorting = False

            self.draw_bars("Sorting Completed")  # Draw the bars in the final state

        if self.record:
            self.save_video()

        pygame.quit()

    def save_video(self):
        import cv2

        height, width, _ = self.frames[0].shape
        out = cv2.VideoWriter('merge_sort_simulation.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, (width, height))

        for frame in self.frames:
            out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

        out.release()
        print("Video saved successfully!")

# Usage
arr = random.sample(range(1, 101), 100)  # Generate 100 unique random integers between 1 and 100
sort_viz = MergeSortVisualization(arr)
sort_viz.visualize()
