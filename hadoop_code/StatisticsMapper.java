import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class StatisticsMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
//	Text shape = new Text();
//	IntWritable one = new IntWritable(1);

	@Override
	protected void map(LongWritable key, Text value, Mapper<LongWritable, Text, Text, IntWritable>.Context context)
			throws IOException, InterruptedException {
		
		// Split the Csv into multiple parts
		String [] columns = value.toString().split(",");
		
		// Get each column from the CSV after splitting.
		String companyName = columns[0];
		String starRating = columns[1];
		String sentiment = columns[2];
		String culture = columns[3];
		String filteredPros = columns[4];

		IntWritable countVal = new IntWritable(1);
		
		if (!companyName.equals("Name")) {
			
			// Case Study 1: Sentiment for each company
			Text sentimentVal = new Text("CASE1_" + companyName + "_" + sentiment + "_sentiment");
			System.out.println("CASE1_" + companyName + "_" + sentiment + "_sentiment");
			context.write(sentimentVal, countVal);
			
			// Case Study 2: Culture for each company
			if (!culture.isEmpty()) {
				Text cultureVal = new Text("CASE2_" + companyName + "_" + culture);
				System.out.println("CASE2_" + companyName + "_" + culture);
				context.write(cultureVal, countVal);
			}
			
			// Case Study 3: WordCloud 
			if (!filteredPros.isEmpty()) {
				
				// Split the review into words
				String[] wordsFromReview = filteredPros.split(" ");
				
				// For each word...
				for (String word : wordsFromReview) {
					word = word.trim();
					if(!word.isEmpty() && !word.contains(" ") && !stringContainsOnlyNumbers(word)) {
						word = word.trim().toLowerCase();
						Text wordVal = new Text("CASE3_" + companyName + "_" + word);
						System.out.println("CASE3_" + companyName + "_" + word);
						context.write(wordVal, countVal);
					}
					
				}
				
			}
			
		}
	}
	
	private boolean stringContainsOnlyNumbers(String str) {
		return str.matches("\\d+");
	}
}
