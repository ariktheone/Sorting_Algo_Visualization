import pygame
import random

class BogoSortVisualization:
    def __init__(self, arr):
        pygame.init()  # Initialize all imported pygame modules
        self.arr = arr
        self.size = len(arr)
        self.window_width = 800
        self.window_height = 600
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Bogo Sort Visualization")
        self.clock = pygame.time.Clock()
        self.done = False
        self.paused = False
        self.record = False
        self.frames = []
        self.speed = 50  # Initial speed
        self.sorting = False

    def is_sorted(self):
        for i in range(1, len(self.arr)):
            if self.arr[i - 1] > self.arr[i]:
                return False
        return True

    def bogo_sort(self):
        while not self.is_sorted():
            random.shuffle(self.arr)

            # Redraw the bars with different colors after each shuffle
            self.draw_bars()
            self.frames.append(pygame.surfarray.array3d(self.screen))  # Record frame
            pygame.display.update()  # Update display after drawing bars
            self.clock.tick(self.speed)  # Adjust the frame rate

    def draw_bars(self, status=""):
        self.screen.fill((50, 50, 50))  # Clear the screen with a background color
        font = pygame.font.Font(None, 24)  # Font for displaying text

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
                        self.speed = min(300, self.speed + 1)  # Increase speed
                    elif event.key == pygame.K_DOWN:
                        self.speed = max(1, self.speed - 1)  # Decrease speed

            if self.sorting and not self.paused:
                self.bogo_sort()  # Perform one step of bogo sort
                self.sorting = False

            self.draw_bars("Sorting Completed")  # Draw the bars in the final state

        if self.record:
            self.save_video()

        pygame.quit()

    def save_video(self):
        import cv2

        height, width, _ = self.frames[0].shape
        out = cv2.VideoWriter('bogo_sort_simulation.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, (width, height))

        for frame in self.frames:
            out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

        out.release()
        print("Video saved successfully!")

# Usage
arr = random.sample(range(1, 11), 10)  # Generate 10 unique random integers between 1 and 10
sort_viz = BogoSortVisualization(arr)
sort_viz.visualize()
