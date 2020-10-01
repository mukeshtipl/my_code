package app;

import org.json.JSONObject;

public class App {
    public static void main(String[] args) throws Exception {
        System.out.println("Hello Java");
        JSONObject obj = new JSONObject("{\"name\": \"Mukesh\"}");
        String my_name = obj.getString("name");
        String x = obj + " Parsed: " + my_name;
        System.out.println(x);
    }
}