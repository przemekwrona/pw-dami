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

        public static int getOptimalValueOfK(List<HeartDataRecord> collection)
        {
            int kNeighboursMax = (int)Math.Floor(Math.Sqrt(collection.Count));
            double[] decisionValues = collection.Select(x => x.classAssigned).Distinct().ToArray();

            // ---------------------------------------------------------------------------
            //inicjalizacja tabeli decisionStrength 
            Dictionary<double, int> decisionStrength = new Dictionary<double, int>();
            foreach (double d in decisionValues)
                decisionStrength.Add(d, 0);

            // ---------------------------------------------------------------------------
            //inicjalizacja tabeli A
            Dictionary<HeartDataRecord, Dictionary<int, double>> A = new Dictionary<HeartDataRecord, Dictionary<int, double>>();
            foreach (HeartDataRecord r in collection)
            {
                A.Add(r, new Dictionary<int, double>());
                for(int kk = 1; kk <= kNeighboursMax; ++kk)
                    A[r].Add(kk, 0);
            }

            // ---------------------------------------------------------------------------
            //początkowe wyznaczenie currentDecision
            double currentDecisionGlobal = double.MinValue;
            int currentDesionGlobalFrequency = 0;
            foreach (double v in decisionValues)
            {
                int freq = collection.FindAll(x => x.classAssigned == v).Count;
                if (freq > currentDesionGlobalFrequency)
                {
                    currentDesionGlobalFrequency = freq;
                    currentDecisionGlobal = v;
                }
            }
            // ---------------------------------------------------------------------------

            foreach (HeartDataRecord record in collection)
            {
                List<double> kNearestDistances = collection.Select(x => x.ComputeDistance(record)).Distinct().OrderBy(x => x).ToList().GetRange(0, kNeighboursMax + 1);
                List<HeartDataRecord> kPlusNN = collection.FindAll(x => kNearestDistances.Contains(x.ComputeDistance(record)));
                double currentDecision = currentDecisionGlobal;
                // usunięcie z listy najbliższych sąsiadów tego samego przetwarzanego rekordu
                kPlusNN.RemoveAll(x => x.ID == record.ID);

                for (int k = 1; k <= kNeighboursMax; ++k)
                {
                    // chwyć k-ty element i zrób z niego regułę
                    Rule rule = new Rule(record, kPlusNN.ElementAt(k - 1));
                    if (rule.IsRuleSatisifiedAgainstCollection(kPlusNN))
                    {
                        double currentValue = kPlusNN.ElementAt(k - 1).classAssigned;
                        decisionStrength[currentValue] += 1;
                        if (decisionStrength[currentValue] > decisionStrength[currentDecision])
                            currentDecision = currentValue;
                    }
                    A[record][k] = currentDecision;
                }


            }

            // ---------------------------------------------------------------------------
            //wyznaczenie kOpt
            int kOpt = -1;
            int setPower = -1;
            for (int k = 1; k <= kNeighboursMax; ++k)
            {
                int currentSetPower = collection.FindAll(x => x.classAssigned == A[x][k]).Count;
                if (currentSetPower > setPower)
                {
                    setPower = currentSetPower;
                    kOpt = k;
                }
            }

            return kOpt;
        }

    }
}
