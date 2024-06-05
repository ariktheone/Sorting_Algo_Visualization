import pygame
import random
import sys

# Define constants for screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define TreeNode class
class TreeNode:
    def __init__(self, value, x, y):
        self.value = value
        self.left = None
        self.right = None
        self.x = x
        self.y = y

# Insert a value into the binary search tree
def insert(root, value, x, y, level):
    if root is None:
        return TreeNode(value, x, y)
    if value < root.value:
        root.left = insert(root.left, value, x - (SCREEN_WIDTH // (2**(level + 1))), y + 50, level + 1)
    else:
        root.right = insert(root.right, value, x + (SCREEN_WIDTH // (2**(level + 1))), y + 50, level + 1)
    return root

# Perform in-order traversal of the binary search tree
def inorder_traversal(root, screen, font):
    if root:
        inorder_traversal(root.left, screen, font)
        # Draw the node value
        node_text = font.render(str(root.value), True, BLACK)
        node_rect = node_text.get_rect(center=(root.x, root.y))
        screen.blit(node_text, node_rect)
        pygame.display.update()
        pygame.time.delay(1000)  # Delay for visualization
        inorder_traversal(root.right, screen, font)

# Create the binary search tree and visualize the sorting process
def tree_sort_visualization(arr):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tree Sort Visualization")
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 30)
    pygame.display.update()

    # Construct the binary search tree
    root = None
    for value in arr:
        root = insert(root, value, SCREEN_WIDTH // 2, 50, 0)

    # Perform in-order traversal to visualize the sorting process
    inorder_traversal(root, screen, font)

    # Wait for user to close window
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

# Usage
arr = random.sample(range(1, 21), 20)  # Generate 20 unique random integers between 1 and 20
tree_sort_visualization(arr)
