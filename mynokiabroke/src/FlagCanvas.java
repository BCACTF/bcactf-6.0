import javax.microedition.lcdui.Canvas;
import javax.microedition.lcdui.Graphics;

public class FlagCanvas extends Canvas {
    public void paint(Graphics graphics) {
        graphics.setColor(0xff0000);
        // for your inconvenience, these lines are drawn in a random order
        graphics.drawLine(140, 10, 160, 10);
        graphics.drawLine(110, 130, 110, 170);
        graphics.drawLine(50, 130, 50, 170);
        graphics.drawLine(10, 110, 30, 110);
        graphics.drawLine(105, 50, 120, 10);
        graphics.drawLine(180, 130, 180, 170);
        graphics.drawLine(50, 110, 70, 110);
        graphics.drawLine(20, 70, 20, 110);
        graphics.drawLine(160, 50, 160, 10);
        graphics.drawLine(90, 10, 105, 50);
        graphics.drawLine(50, 10, 70, 10);
        graphics.drawLine(10, 10, 30, 10);
        graphics.drawLine(120, 50, 120, 10);
        graphics.drawLine(150, 130, 150, 170);
        graphics.drawLine(140, 50, 160, 50);
        graphics.drawLine(10, 130, 30, 130);
        graphics.drawLine(90, 170, 110, 170);
        graphics.drawLine(50, 70, 50, 90);
        graphics.drawLine(30, 150, 20, 150);
        graphics.drawLine(30, 150, 30, 170);
        graphics.drawLine(90, 150, 110, 150);
        graphics.drawLine(50, 150, 70, 170);
        graphics.drawLine(20, 10, 20, 50);
        graphics.drawLine(140, 30, 160, 30);
        graphics.drawLine(20, 50, 10, 50);
        graphics.drawLine(70, 90, 70, 110);
        graphics.drawLine(50, 70, 70, 70);
        graphics.drawLine(170, 130, 190, 130);
        graphics.drawLine(50, 25, 50, 50);
        graphics.drawLine(10, 170, 30, 170);
        graphics.drawLine(10, 170, 10, 130);
        graphics.drawRect(50, 130, 20, 20);
        graphics.drawLine(90, 130, 110, 130);
        graphics.drawLine(70, 10, 70, 25);
        graphics.drawLine(150, 150, 130, 150);
        graphics.drawLine(50, 25, 70, 25);
        graphics.drawLine(10, 90, 20, 70);
        graphics.drawLine(90, 10, 90, 50);
        graphics.drawLine(130, 130, 130, 150);
        graphics.drawLine(70, 90, 50, 90);
        graphics.drawLine(50, 50, 70, 50);
    }
}
