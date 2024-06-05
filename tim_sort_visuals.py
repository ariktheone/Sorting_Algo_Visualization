import pygame
import random

class TimSortVisualization:
    def __init__(self, arr):
        pygame.init()  # Initialize all imported pygame modules
        self.arr = arr
        self.size = len(arr)
        self.window_width = 800
        self.window_height = 600
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Tim Sort Visualization")
        self.clock = pygame.time.Clock()
        self.done = False
        self.paused = False
        self.record = False
        self.frames = []
        self.speed = 0.001  # Initial speed
        self.sorting = False

    def timsort(self):
        minrun = self.calc_minrun(self.size)
        for start in range(0, self.size, minrun):
            end = min(start + minrun, self.size)
            self.insertion_sort(start, end)
        size = minrun
        while size < self.size:
            for start in range(0, self.size, size * 2):
                mid = min(self.size, start + size)
                end = min(self.size, mid + size)
                self.merge(start, mid, end)
            size *= 2

    def insertion_sort(self, start, end):
        for i in range(start + 1, end):
            key = self.arr[i]
            j = i - 1
            while j >= start and self.arr[j] > key:
                self.arr[j + 1] = self.arr[j]
                j -= 1
            self.arr[j + 1] = key

    def merge(self, start, mid, end):
        left = self.arr[start:mid]
        right = self.arr[mid:end]
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                self.arr[start + k] = left[i]
                i += 1
            else:
                self.arr[start + k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            self.arr[start + k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            self.arr[start + k] = right[j]
            j += 1
            k += 1

    def calc_minrun(self, n):
        r = 0
        while n >= 64:
            r |= n & 1
            n >>= 1
        return n + r

    def draw_bars(self, status=""):
        self.screen.fill((50, 50, 50))  # Clear the screen with a background color
        font = pygame.font.Font(None, 24)  # Font for displaying text

        max_height = max(self.arr)
        for i, height in enumerate(self.arr):
            normalized_height = height / max_height * self.window_height
            bar_rect = pygame.Rect(i * (self.window_width // self.size), self.window_height - normalized_height, self.window_width // self.size, normalized_height)
            pygame.draw.rect(self.screen, (255, 255, 255), bar_rect)

        # Display sorting status
        status_text = font.render(status, True, (255, 255, 255))
        self.screen.blit(status_text, (10, 10))

        pygame.display.update()  # Update display after drawing bars

    def visualize(self):
        self.sorting = True
        self.timsort()
        self.draw_bars("Sorting Completed")
        if self.record:
            self.save_video()

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

            if self.record:
                self.save_video()

        pygame.quit()

    def save_video(self):
        import cv2

        height, width, _ = self.frames[0].shape
        out = cv2.VideoWriter('tim_sort_simulation.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, (width, height))

        for frame in self.frames:
            out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

        out.release()
        print("Video saved successfully!")

# Usage
arr = random.sample(range(1, 101), 100)  # Generate 100 unique random integers between 1 and 100
sort_viz = TimSortVisualization(arr)
sort_viz.visualize()
