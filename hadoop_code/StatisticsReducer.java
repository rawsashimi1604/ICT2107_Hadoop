import java.io.IOException;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map.Entry;
import java.util.TreeMap;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class StatisticsReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
	IntWritable totalIW = new IntWritable();
    private HashMap<Text, IntWritable> sentimentMap = new HashMap<Text, IntWritable>();
	
    
    // For each mapped input...
	@Override
	protected void reduce(Text key, Iterable<IntWritable> values,
			Reducer<Text, IntWritable, Text, IntWritable>.Context context)
		throws IOException, InterruptedException
	{
		int total = 0;
		
		// For each valHASHMAP VALUES:
		for(IntWritable value: values){
			total += value.get();
		}
		
		totalIW.set(total);
		context.write(key, totalIW);
		
	}
}
 