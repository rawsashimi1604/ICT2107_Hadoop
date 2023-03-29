import java.io.IOException;
import java.util.Date;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class StatisticsAnalysis {
	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf, "StatisticsAnalysis");
		job.setJarByClass(StatisticsAnalysis.class);
		job.setMapperClass(StatisticsMapper.class);
		job.setCombinerClass(StatisticsReducer.class);
		job.setReducerClass(StatisticsReducer.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(IntWritable.class);
		
		Path byteDanceCsv = new Path("hdfs://localhost:9000/project/input/ByteDance.csv");
		Path ibmCsv = new Path("hdfs://localhost:9000/project/input/IBM.csv");
		Path microsoftCsv = new Path("hdfs://localhost:9000/project/input/Microsoft.csv");
		Path ncsCsv = new Path("hdfs://localhost:9000/project/input/NCS.csv");
		Path sapCsv = new Path("hdfs://localhost:9000/project/input/SAP.csv");
		
		Path outputPath = new Path("hdfs://localhost:9000/project/output" + new Date().getTime());

		
		// Take in CSVs as input to hadoop...
		FileInputFormat.addInputPath(job, byteDanceCsv);
		FileInputFormat.addInputPath(job, ibmCsv);
		FileInputFormat.addInputPath(job, microsoftCsv);
		FileInputFormat.addInputPath(job, ncsCsv);
		FileInputFormat.addInputPath(job, sapCsv);
//		
		FileOutputFormat.setOutputPath(job, outputPath);

		System.exit((job.waitForCompletion(true)) ? 0 : 1);
	}
}
