import com.sun.kvem.netmon.HttpAgent;

import javax.microedition.lcdui.*;
import javax.microedition.midlet.MIDlet;
import javax.microedition.midlet.MIDletStateChangeException;

public class AppMIDlet extends MIDlet implements CommandListener {
    private static final Command PASSWD_COMMAND = new Command("Enter Password", Command.ITEM, 1);

    Form form;
    TextField textField;
    FlagCanvas fc = new FlagCanvas();
    protected void startApp() throws MIDletStateChangeException {
        form = new Form("");
        textField = new TextField("Enter Password:", "", 10, 65536);
        form.addCommand(PASSWD_COMMAND);
        form.setCommandListener(this);
        form.append(textField);
        Display.getDisplay(this).setCurrent(form);
    }

    protected void pauseApp() {
    }

    protected void destroyApp(boolean b) throws MIDletStateChangeException {
    }

    public void commandAction(Command command, Displayable displayable) {
        if (command == PASSWD_COMMAND) {
            if (textField.getString().equals("This is a very long password OoOOoOOOoOOOoOOOoOoOooOooooOOOoo")) {
                Display.getDisplay(this).setCurrent(fc);
            }
        }
    }
}
