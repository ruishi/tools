import java.io.*;
import java.util.*;

public class Delta
{
    public static void main(String[] args)
    {
	String choiceType = "";
	String filename = "";

	if (args.length == 0)
	{
	    System.out.println("Usage: ChoiceMaker [-o|r|rs|d] <filename>");
	    System.exit(0);
	}
	else if(args.length == 1)
	{
	    System.out.println("Usage: ChoiceMaker [-o|r|rs|d] <filename>");
	    
	}
	else
	{
	    choiceType = args[0];
	    filename = args[1];
	    switch(choiceType.toLowerCase())
	    {
	    case "-o":
		justOnce(filename);
		break;
	    case "-r":
		repeatable(filename);
		break;
	    case "-rs":
		restart(filename);
		break;
	    case "-d":
		deltafy(filename);
		break;
	    default:
		System.out.println("Usage: ChoiceMaker [-o|r|rs] <filename>");
	    }
	}
    }

    public static void justOnce(String filename)
    {
	String line;
	ArrayList<String> choices = new ArrayList<String>();
	ArrayList<String> nonchoices = new ArrayList<String>();

	BufferedReader input;
	BufferedWriter output;

	try
	{
	    input = new BufferedReader(new FileReader(filename));
	    while((line = input.readLine()) != null)
	    {
		if(line.startsWith(">>"))
		    choices.add(line.replaceFirst(">>",""));
		else
		    nonchoices.add(line);
	    }
	    input.close();
	}
	catch(IOException e) {}

	if(!choices.isEmpty())
	{
	    MersenneTwisterFast rChoice = new MersenneTwisterFast();
	    int fc = rChoice.nextInt(choices.size()); //final choice
	    System.out.println("Go with " + choices.get(fc) + "!");
	    for(int i = 0; i < choices.size(); i++)
	    {
		choices.set(i,">>" + choices.get(i));
	    }
	    String temp = (choices.get(fc)).replaceFirst(">>","<<");
	    choices.set(fc, temp);
	    
	    try
	    {
		output = new BufferedWriter(new FileWriter(filename));
		for(int i = 0; i < choices.size(); i++)
		{
		    output.write(choices.get(i));
		    output.newLine();
		}
		for(int j = 0; j < nonchoices.size(); j++)
		{
		    output.write(nonchoices.get(j));
		    output.newLine();
		}
		output.close();
	    }
	    catch(IOException e) {}
	}
	else 
	    System.out.println("You have nothing to choose from, you dork!");
    }

    public static void repeatable(String filename)
    {
	String line;
	ArrayList<String> choices = new ArrayList<String>();

	BufferedReader input;

	try
	{
	    input = new BufferedReader(new FileReader(filename));
	    while((line = input.readLine()) != null)
	    {
		if(line.startsWith(">>"))
		    choices.add(line.replaceFirst(">>",""));
		else if(line.startsWith("<<"))
		    choices.add(line.replaceFirst("<<",""));
	    }
	    input.close();
	}
	catch(IOException e) {}

	if(!choices.isEmpty())
	{
	    MersenneTwisterFast rChoice = new MersenneTwisterFast();
	    int fc = rChoice.nextInt(choices.size()); //final choice
	    System.out.println("Go with " + choices.get(fc) + "!");
	}
	else
	    System.out.println("You have nothing to choose from, you dork!");

    }

    public static void restart(String filename)
    {
	String line;
	ArrayList<String> choices = new ArrayList<String>();

	BufferedReader input;
	BufferedWriter output;

	try
	{
	    input = new BufferedReader(new FileReader(filename));
	    while((line = input.readLine()) != null)
	    {
		choices.add(line);
	    }
	    input.close();

	    output = new BufferedWriter(new FileWriter(filename));

	    for(int i = 0; i < choices.size(); i++)
	    {
		output.write(choices.get(i).replaceFirst("<<",">>"));
		output.newLine();
	    }
	    output.close();
	}
	catch(IOException e) {}
    }

    public static void deltafy(String filename)
    {
	String line;
	ArrayList<String> choices = new ArrayList<String>();

	BufferedReader input;
	BufferedWriter output;

	try
	{
	    input = new BufferedReader(new FileReader(filename));
	    while((line = input.readLine()) != null)
	    {
		choices.add(line);
	    }
	    input.close();

	    output = new BufferedWriter(new FileWriter(filename));

	    for(int i = 0; i < choices.size(); i++)
	    {
		if(!choices.get(i).startsWith(">>"))
		{
		    output.write(">>" + choices.get(i));
		}
		else
		    output.write(choices.get(i));
		output.newLine();
	    }
	    output.close();
	}
	catch(IOException e) {}
    }
   

}
