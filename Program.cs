using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DAMI
{
    class Program
    {
        static void Main(string[] args)
        {
            
            List<HeartDataRecord> records = new List<HeartDataRecord>();

            NumberFormatInfo provider = new NumberFormatInfo();
            provider.NumberDecimalSeparator = ".";
            provider.NumberGroupSeparator = ",";


            // creating
            foreach (string line in System.IO.File.ReadLines(@"C:\Users\amata\Desktop\DAMI Lectures\PROJECT\heart.dat"))
            {
                records.Add(new HeartDataRecord(line.Replace("\n", "").Replace("\r", ""), provider));
            }
            int kNeighbours = (int)Math.Floor(Math.Sqrt(records.Count));

            HeartDataRecord source = records.Find(x => x.ID == 1);

            List<double> kNearestDistances = records.Select(x => x.ComputeDistance(source)).Distinct().OrderBy(x => x).ToList().GetRange(0, kNeighbours + 1);
            List<HeartDataRecord> kPlusNN = records.FindAll(x => kNearestDistances.Contains(x.ComputeDistance(source)));
            // techniczna rzecz (do usunięcia)
            kPlusNN.RemoveAll(x => x.ID == source.ID);

            List<HeartDataRecord> kPlusNNFiltered = new List<HeartDataRecord>();
            foreach (HeartDataRecord record in kPlusNN)
            {
                Rule rule = new Rule(source, record);
                if (rule.IsRuleSatisifiedAgainstCollection(kPlusNN)) kPlusNNFiltered.Add(record);
            }


            double nominatorOne = kPlusNNFiltered.FindAll(x => x.classAssigned == 1.0).Count;
            double nominatorTwo = kPlusNNFiltered.FindAll(x => x.classAssigned == 2.0).Count;
            double denominatorOne = records.FindAll(x => x.classAssigned == 1.0).Count;
            double denominatorTwo = records.FindAll(x => x.classAssigned == 2.0).Count;

            double assignedClass = nominatorOne > nominatorTwo ? 1.0 : 2.0;
            double assignedClassReferential = ((nominatorOne / denominatorOne) > (nominatorTwo / denominatorTwo)) ? 1.0 : 2.0;

            Console.WriteLine("Assigned class: {0}", assignedClass);
            Console.WriteLine("Assigned class referential: {0}", assignedClassReferential);

            int optK = HeartDataRecord.getOptimalValueOfK(records);
            Console.WriteLine("Optimal K value: {0}", optK);

            return;
        }
    }
}
