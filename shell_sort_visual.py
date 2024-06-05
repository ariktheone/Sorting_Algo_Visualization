import pygame
import random

class ShellSortVisualization:
    def __init__(self, arr):
        pygame.init()  # Initialize all imported pygame modules
        self.arr = arr
        self.size = len(arr)
        self.window_width = 800
        self.window_height = 600
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Shell Sort Visualization")
        self.clock = pygame.time.Clock()
        self.colors = [(255, 255, 255) for _ in range(self.size)]  # Initial color for each bar
        self.bar_width = self.window_width // self.size
        self.max_height = max(self.arr)
        self.done = False
        self.paused = False
        self.record = False
        self.frames = []
        self.speed = 50  # Initial speed
        self.sorting = False

    def shell_sort(self):
        n = len(self.arr)
        gap = n // 2

        while gap > 0:
            for i in range(gap, n):
                temp = self.arr[i]
                j = i
                while j >= gap and self.arr[j - gap] > temp:
                    self.arr[j] = self.arr[j - gap]
                    j -= gap

                    # Redraw the bars with different colors after each swap
                    self.colors = [(0, 255, 0) if k == j or k == j - gap else (255, 255, 255) for k in range(self.size)]
                    self.draw_bars(f"Swapping: {self.arr[j]} and {self.arr[j - gap]}")
                    self.frames.append(pygame.surfarray.array3d(self.screen))  # Record frame
                    pygame.display.update()  # Update display after drawing bars
                    self.clock.tick(self.speed)  # Adjust the frame rate

                self.arr[j] = temp

            gap //= 2

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
        self.shell_sort()
        self.colors = [(0, 255, 0) for _ in range(self.size)]  # Set the color for sorted bars
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
        out = cv2.VideoWriter('shell_sort_simulation.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, (width, height))

        for frame in self.frames:
            out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

        out.release()
        print("Video saved successfully!")

# Usage
arr = random.sample(range(1, 101), 100)  # Generate 100 unique random integers between 1 and 100
sort_viz = ShellSortVisualization(arr)
sort_viz.visualize()
