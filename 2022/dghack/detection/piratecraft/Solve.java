import java.nio.charset.StandardCharsets;
import java.util.Base64;

// 
// Decompiled by Procyon v0.5.36
// 

public class Solve {
    public static void main(String[] args) {
        final String str = "";
        final int[] array = { 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 119, 61, 61 };
        final int[] array2 = { 73, 121, 65, 116, 73, 67, 48, 103, 76, 83, 65, 116, 73, 67, 48, 103, 73, 70, 100, 70, 84, 69, 78, 80, 84, 85, 85, 103, 83, 85, 52, 103, 85, 48, 104, 70, 84, 69, 119, 103, 76, 83, 65, 116, 73, 67, 48, 103, 76, 83, 65, 116, 73, 67, 48, 103, 73, 119, 61, 61 };
        final int[] array3 = { 73, 121, 65, 116, 73, 67, 48, 103, 81, 85, 120, 77, 73, 70, 108, 80, 86, 86, 73, 103, 81, 49, 86, 67, 82, 86, 77, 103, 81, 86, 74, 70, 73, 69, 74, 70, 84, 69, 57, 79, 82, 121, 66, 85, 84, 121, 66, 86, 85, 121, 65, 116, 73, 67, 48, 103, 73, 119, 61, 61 };
        final int[] array4 = { 73, 121, 65, 116, 76, 83, 65, 107, 83, 71, 70, 106, 97, 50, 86, 107, 88, 50, 74, 53, 88, 51, 86, 117, 97, 71, 70, 119, 99, 72, 107, 117, 89, 50, 57, 116, 99, 71, 86, 48, 97, 88, 82, 118, 99, 105, 53, 106, 98, 50, 48, 103, 76, 83, 48, 103, 73, 119, 61, 61 };
        final int[] array5 = { 73, 121, 66, 69, 82, 48, 104, 66, 81, 48, 116, 55, 78, 68, 69, 120, 88, 49, 107, 119, 86, 88, 74, 102, 81, 49, 85, 52, 77, 122, 86, 102, 78, 72, 73, 122, 88, 122, 103, 122, 77, 84, 66, 79, 78, 108, 56, 51, 77, 70, 57, 86, 78, 88, 48, 103, 73, 119, 61, 61 };
        final int[] array6 = { 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 121, 77, 106, 73, 119, 61, 61 };
        String string = "";
        final int[] array7 = array;
        for (int length = array7.length, i = 0; i < length; ++i) {
            string += (char)array7[i];
        }
        final String string2 = str + new String(Base64.getDecoder().decode(string), StandardCharsets.UTF_8) + "\r\n";
        String string3 = "";
        final int[] array8 = array2;
        for (int length2 = array8.length, j = 0; j < length2; ++j) {
            string3 += (char)array8[j];
        }
        final String string4 = string2 + new String(Base64.getDecoder().decode(string3), StandardCharsets.UTF_8) + "\r\n";
        String string5 = "";
        final int[] array9 = array3;
        for (int length3 = array9.length, k = 0; k < length3; ++k) {
            string5 += (char)array9[k];
        }
        final String string6 = string4 + new String(Base64.getDecoder().decode(string5), StandardCharsets.UTF_8) + "\r\n";
        String string7 = "";
        final int[] array10 = array4;
        for (int length4 = array10.length, l = 0; l < length4; ++l) {
            string7 += (char)array10[l];
        }
        final String string8 = string6 + new String(Base64.getDecoder().decode(string7), StandardCharsets.UTF_8) + "\r\n";
        String string9 = "";
        final int[] array11 = array5;
        for (int length5 = array11.length, n = 0; n < length5; ++n) {
            string9 += (char)array11[n];
        }
        final String string10 = string8 + new String(Base64.getDecoder().decode(string9), StandardCharsets.UTF_8) + "\r\n";
        String string11 = "";
        final int[] array12 = array6;
        for (int length6 = array12.length, n2 = 0; n2 < length6; ++n2) {
            string11 += (char)array12[n2];
        }
        System.out.println(string10 + new String(Base64.getDecoder().decode(string11), StandardCharsets.UTF_8) + "\r\n");
        
        
    }
            
}
