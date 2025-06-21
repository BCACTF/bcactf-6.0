from sympy import divisors

from PIL import Image, ImageDraw

def draw_factors_image(num, off_scale=0, width=20, height_per_row=10, branch_length=12, branch_gap=6):
    factors = set(divisors(num))
    img_height = num * height_per_row
    # Allow extra width for branches
    max_branch = num // 2
    img_width = width + (branch_length + branch_gap) * (max_branch + 1)
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)
    prev_was_line = False
    i = 1
    while i <= num:
        y = img_height - ((i - 1) * height_per_row + height_per_row // 2)
        x = width // 2
        if i in factors:
            # Draw vertical line
            draw.line([(x, y - height_per_row // 2), (x, y + height_per_row // 2)], fill="black", width=2)
            if prev_was_line:
                y_prev = y + height_per_row
                draw.line([(x - 3, y_prev), (x + 3, y_prev)], fill="black", width=2)
            prev_was_line = True
            i += 1
        else:
            # Find run of consecutive dots
            start = i
            while i <= num and i not in factors:
                i += 1
            run_length = i - start
            # Draw single dot for the run
            y_start = img_height - ((start - 1) * height_per_row + height_per_row // 2)
            draw.ellipse([(x - 2, y_start - 2), (x + 2, y_start + 2)], fill="black")
            # Draw horizontal line to branch
            x_branch = x + branch_length + branch_gap
            draw.line([(x + 2, y_start), (x_branch, y_start)], fill="black", width=2)
            # Draw branch vertically stacked, including factors as dots
            for b in range(run_length):
                y_branch = y_start + (b * height_per_row)
                # Draw vertical connector for branch
                if b > 0:
                    y_prev_branch = y_start + ((b - 1) * height_per_row)
                    draw.line([(x_branch, y_prev_branch), (x_branch, y_branch)], fill="black", width=2)
                n = start + b
                # On the branch: dot if factor, vertical line if not
                if n in factors:
                    draw.ellipse([(x_branch - 2, y_branch - 2), (x_branch + 2, y_branch + 2)], fill="black")
                else:
                    draw.line([(x_branch, y_branch - height_per_row // 2), (x_branch, y_branch + height_per_row // 2)], fill="black", width=2)
            prev_was_line = False
    img.save("factors.png")
    print("Image saved as factors.png")

draw_factors_image(20)