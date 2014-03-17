import java.io.*;
import java.util.*;

public class Delta
{
    public static void main(String[] args)
    {
	String choiceType = null;
	String filename = null;
	String usage = "Usage: Delta [-h] ("
	    + "-r REPEAT | "
	    + "-rs RESTART | "
	    + "-d DELTAFY) "
	    + "<filename>";

	if (args.length == 0 || args.length > 2) 
	{
	    System.out.println(usage);
	    System.exit(0);
	}
	else if (args.length == 1)
	{
	    if ("-h".equals(args[0]))
	    {
		choiceType = args[0];
	    }
	    else
	    {
		choiceType="default";
		filename = args[0];
	    }
	}
	else
	{
	    choiceType = args[0];
	    filename = args[1];
	}
	    
	switch(choiceType.toLowerCase())
	{
	    case "-r":
		repeat(filename);
		break;
	    case "-rs":
		restart(filename);
		break;
	    case "-d":
		deltafy(filename);
		break;
	    case "-h":
		String descriptor = "\nMakes a decision given a list of choices.\n";
		System.out.println(usage);
		System.out.println(descriptor);
		System.out.print("Positional arguments:");
		printArgs("filename", "The name of the file which has the choices."
			  + "There should be one choice per line.\n");
		System.out.print("\nOptional arguments:");
		printArgs("-h", "Show this help message and exit");
		printArgs("-r", "Allow for repeat choices. By default, Delta skips"
			  + " over any options chosen in");
		printArgs("", "previous runs. Note this option does not reset the \"chosen\" flag for any ");
		printArgs("","previously chosen items in the file.");
		printArgs("-rs", "\"Restart\" a file if you've exhausted all the choices without using" 
			  + " the repeat flag.");
		printArgs("-d", "\"Deltafy.\" Delta uses \'>>\' and \'<<\' as markers to denote whether a" 
			  + " choice has been");
		printArgs("", "previously chosen or not. This will automatically add  \'>>\' to each choice" 
			  + " in a file.");
		printArgs("", "Currently these markers are required for Delta to parse a file.\n");
		break;
	    default:
		once(filename);
	}
    }

    public static void printArgs(String argument, String description)
    {
	System.out.printf("\n%-8s %-40s", argument, description);
    }

    public static void once(String filename)
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
	    Random rChoice = new Random(System.currentTimeMillis());
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
	    System.out.println("You have nothing to choose from!");
    }

    public static void repeat(String filename)
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
	    Random rChoice = new Random(System.currentTimeMillis());
	    int fc = rChoice.nextInt(choices.size()); //final choice
	    System.out.println("Go with " + choices.get(fc) + "!");
	}
	else
	    System.out.println("You have nothing to choose from!");

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
