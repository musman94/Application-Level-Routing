import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.BufferedInputStream;
import java.io.IOException;
import java.net.Socket;
import java.net.ServerSocket;
import java.net.InetAddress;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;
import java.nio.ByteBuffer;
import java.lang.Short;
import java.util.HashMap;

public class Router {

    public static void main(String[] args) throws IOException {

        String routerIp = args[0].split(":")[0];
        int routerPort = Integer.parseInt(args[0].split(":")[1]);
        InetAddress addr = InetAddress.getByName(routerIp);
        HashMap<String, String> opMap = new HashMap<String, String>();
        String key = "";

        for(int i = 1; i < args.length; i++) {
            if(i % 2 == 1)
                key = args[i];
            if(i % 2 == 0) 
                opMap.put(key, args[i]);
        }

        ServerSocket routerSocket = new ServerSocket(routerPort, 0, addr);
        Socket router = routerSocket.accept();
        DataOutputStream outToClient = new DataOutputStream(router.getOutputStream());
        DataInputStream inFromClient = new DataInputStream(new BufferedInputStream(router.getInputStream()));

        Socket opSocket;
		DataOutputStream outToOp;
		DataInputStream inFromOp;
        String incoming = "";
        String opIp = "";
        int opPort;
        String data = "";
        byte[] dataBytes = null;
        String[] ops = null;

        while(true) {
        	incoming = inFromClient.readLine();
        	data = incoming.split(" ")[0];
        	dataBytes = data.getBytes(StandardCharsets.US_ASCII);
        	ops = incoming.split(" ")[1].split(":")[1].split(",");
        	for(int i = 0; i < ops.length; i++) {
        		if(opMap.containsKey(ops[i])) {
        			opIp = opMap.get(ops[i]).split(":")[0];
        			opPort = Integer.parseInt(opMap.get(ops[i]).split(":")[1]);
        			opSocket = new Socket(InetAddress.getByName(opIp), opPort);
        			outToOp = new DataOutputStream(opSocket.getOutputStream());
        			inFromOp = new DataInputStream(new BufferedInputStream(opSocket.getInputStream()));
        			outToOp.write(dataBytes);
        			data = inFromOp.readLine();
        			dataBytes = data.getBytes(StandardCharsets.US_ASCII);
        			opSocket.close();
        		}
        	}
        	int number = Integer.parseInt(data.split(":")[1]);
        	String numberOfZeros = Integer.toString(8 - (int) Math.log10(number) + 1);
        	String formattedNumber = String.format("%0" + numberOfZeros + "d", number);
        	data = data.split(":")[0] + ":" + formattedNumber;
        	dataBytes = data.getBytes(StandardCharsets.US_ASCII);
        	outToClient.write(dataBytes);
        	break;
        }
        router.close(); 
   }
}

