using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DAMI
{
    public class HeartDataRecord
    {
        private static int currentID = 1;
        private static string[] recordFields = { "age", "sex", "chestPainType", "restingBloodPressure", "serumCholesterol", "fastingBloodSugar", "restingElectrocardiographicResults", "maximumHeartRate", "exerciseInducedAngina", "oldPeak", "theSlopeOfPeak", "noMajorVessels", "thal", "classAssigned" };
        private static bool[] isRecordFieldTypeNumeric = { true, false, false, true, true, false, false, true, false, true, false, true, false, false };
        private static Dictionary<string, double> mins = new Dictionary<string, double>()
        {
            { "age", Double.MaxValue },
            { "sex", Double.MaxValue },
            { "chestPainType", Double.MaxValue },
            { "restingBloodPressure", Double.MaxValue },
            { "serumCholesterol", Double.MaxValue },
            { "fastingBloodSugar", Double.MaxValue },
            { "restingElectrocardiographicResults", Double.MaxValue },
            { "maximumHeartRate", Double.MaxValue },
            { "exerciseInducedAngina", Double.MaxValue },
            { "oldPeak", Double.MaxValue },
            { "theSlopeOfPeak", Double.MaxValue },
            { "noMajorVessels", Double.MaxValue },
            { "thal", Double.MaxValue },
            { "classAssigned", Double.MaxValue }
        };

        private static Dictionary<string, double> maxes = new Dictionary<string, double>()
        {
            { "age", Double.MinValue },
            { "sex", Double.MinValue },
            { "chestPainType", Double.MinValue },
            { "restingBloodPressure", Double.MinValue },
            { "serumCholesterol", Double.MinValue },
            { "fastingBloodSugar", Double.MinValue },
            { "restingElectrocardiographicResults", Double.MinValue },
            { "maximumHeartRate", Double.MinValue },
            { "exerciseInducedAngina", Double.MinValue },
            { "oldPeak", Double.MinValue },
            { "theSlopeOfPeak", Double.MinValue },
            { "noMajorVessels", Double.MinValue },
            { "thal", Double.MinValue },
            { "classAssigned", Double.MinValue }
        };

        public int ID;
        public double age;
        public double sex;
        public double chestPainType;
        public double restingBloodPressure;
        public double serumCholesterol;
        public double fastingBloodSugar;
        public double restingElectrocardiographicResults;
        public double maximumHeartRate;
        public double exerciseInducedAngina;
        public double oldPeak;
        public double theSlopeOfPeak;
        public double noMajorVessels;
        public double thal;
        public double classAssigned;

        public HeartDataRecord(string row, NumberFormatInfo provider)
        {
            ID = currentID;
            ++currentID;

            string[] rowSplitted = row.Split(' ');
            var classType = typeof(HeartDataRecord);

            int column = 0;
            foreach (string fieldName in recordFields)
            {
                double currentValue = Convert.ToDouble(rowSplitted[column], provider);
                classType.GetField(fieldName).SetValue(this, currentValue);
                

                if (isRecordFieldTypeNumeric[column])
                {
                    if (currentValue > maxes[fieldName]) maxes[fieldName] = currentValue;
                    if (currentValue < mins[fieldName]) mins[fieldName] = currentValue;
                }

                ++column;
            }
            return;

        }

        public double ComputeDistance(HeartDataRecord target)
        {
            double distance = 0.0;
            var classType = typeof(HeartDataRecord);

            int column = 0;
            foreach (string fieldName in recordFields)
            {
                if (fieldName != "classAssigned")
                {
                    double sourceFieldValue = (double)classType.GetField(fieldName).GetValue(this);
                    double targetFieldValue = (double)classType.GetField(fieldName).GetValue(target);
                    double minFieldValue = mins[fieldName];
                    double maxFieldValue = maxes[fieldName];


                    if (isRecordFieldTypeNumeric[column])
                    {
                        distance += Math.Abs((sourceFieldValue - targetFieldValue) / (minFieldValue - maxFieldValue));
                    }
                    else
                    {
                        if (sourceFieldValue != targetFieldValue) distance += 1.0;
                    }
                }
                ++column;
            }

            return distance;
        }

        public static string[] getFields()
        {
            return recordFields;
        }

        public static bool[] getIsRecordFieldTypeNumeric()
        {
            return isRecordFieldTypeNumeric;
        }

        public static double getMaxAge()
        {
            return maxes["age"];
        }

        public static double getMinAge()
        {
            return mins["age"];
        }


    }
}
