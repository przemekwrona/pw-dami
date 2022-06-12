using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DAMI
{
    public enum ConditionType
    {
        Interval,
        Equation
    }

    public class Condition
    {
        public string fieldName;
        public double min;
        public double max;
        public double equalValue;
        public ConditionType conditionType;

        public Condition(string _fieldName, double _equalValue)
        {
            fieldName = _fieldName;
            equalValue = _equalValue;
            conditionType = ConditionType.Equation;
            min = double.MaxValue;
            max = double.MinValue;
            return;
        }

        public Condition(string _fieldName, double _min, double _max)
        {
            fieldName = _fieldName;
            min = _min;
            max = _max;
            conditionType = ConditionType.Interval;
            equalValue = double.MaxValue;
            return;
        }

        public bool IsConditionSatisfied(HeartDataRecord record)
        {
            var classType = typeof(HeartDataRecord);
            double value = (double)classType.GetField(fieldName).GetValue(record);

            if (conditionType == ConditionType.Equation)
            {
                return value == equalValue;
            }
            else
            {
                return (min <= value) && (value <= max);
            }
        }

    }

    public class Rule
    {
        private List<Condition> conditions;
        public double classAssigned;

        public Rule(HeartDataRecord source, HeartDataRecord neighbour)
        {
            conditions = new List<Condition>();
            classAssigned = neighbour.classAssigned;

            int column = 0;
            var classType = typeof(HeartDataRecord);
            foreach (string field in HeartDataRecord.getFields())
            {
                double sourceValue = (double)classType.GetField(field).GetValue(source);
                double neighbourValue = (double)classType.GetField(field).GetValue(neighbour);

                if (HeartDataRecord.getIsRecordFieldTypeNumeric()[column])
                {
                    conditions.Add(new Condition(field, Math.Min(sourceValue, neighbourValue), Math.Max(sourceValue, neighbourValue)));
                }
                else
                {
                    if(sourceValue == neighbourValue) conditions.Add(new Condition(field, sourceValue));
                }

                ++column;
            }

            return;
        }

        public void AddCondition(Condition c)
        {
            conditions.Add(c);
            return;
        }

        public bool IsRuleSatisfied(HeartDataRecord record)
        {
            foreach (Condition c in conditions)
                if (!c.IsConditionSatisfied(record)) return false;

            return true;
        }

        public bool IsRuleSatisifiedAgainstCollection(List<HeartDataRecord> collection)
        {
            foreach (HeartDataRecord record in collection.FindAll(x => x.classAssigned != classAssigned))
                if (IsRuleSatisfied(record)) return false;

            return true;
        }

    }
}
