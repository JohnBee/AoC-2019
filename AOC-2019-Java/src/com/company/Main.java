package com.company;
import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;


public class Main {

    public static void main(String[] args){
        Day1.day1();
    }
}

class Day1 {
    public static void day1(){
        System.out.println(calcTotalFuel());
        System.out.println(calcTotalFuelPart2());
    }
    public static Integer calcFuel(Integer mass){
        Integer a = (mass/3) - 2;
        if(a < 0) a = 0;
        return a;
    }
    public static Integer[] readFile() throws IOException {
        BufferedReader f = new BufferedReader(new FileReader("src/com/company/day1input.txt"));
        List<Integer> intList = new ArrayList<Integer>();
        String line;
        while ((line = f.readLine()) != null) {
            Integer I = Integer.parseInt(line);
            intList.add(I);
        }
        f.close();
        Integer[] intArray = intList.toArray(new Integer[]{});
        return intArray;
    }
    public static Integer calcTotalFuel(){
        Integer total = 0;
        try {
            Integer[] masses = readFile();
            for(Integer i: masses){
                total += calcFuel(i);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return total;
    }
    public static Integer calcTotalFuelPart2(){
        Integer total = 0;
        try {
            Integer[] masses = readFile();
            for(Integer i: masses){
                total += part2(i);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return total;
    }
    public static Integer part2(Integer fuel){
        if(fuel == 0){
            return 0;
        }
        else{
            return calcFuel(fuel) + part2(calcFuel(fuel));
        }
    }
}