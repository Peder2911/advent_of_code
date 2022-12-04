/* Advent of Code 2022 04
 *
 * Attempt at writing a verbose and ceremonious C# solution.
 * As you can see, I am not a Java / C# dev!
 *
 * Tested with mcr.microsoft.com/dotnet/sdk:6.0
 */

namespace Fourth 
{
   class Span
   {
      public int Start {get; set;}
      public int End {get; set;}

      public Span(int start, int end)
      {
         this.Start = start;
         this.End = end;
      }

      public static Span Parse(string raw)
      {
         var parsed = raw.Split("-",2);
         return new Span(Int32.Parse(parsed[0]), Int32.Parse(parsed[1]));

      }
      public int Length()
      {
         return this.End - this.Start;
      }

      public int[] Numbers()
      {
         int[] numbers = new int[this.Length()];
         for (var i = 0; i <= this.Length(); i++)
         {
            numbers[i] = i + this.Start;
         }
         return numbers;
      }

      public Span? Intersection(Span other)
      {
         if(this.Overlaps(other))
         {
            return new Span(Math.Max(this.Start,other.Start), Math.Min(this.End, other.End));
         }
         else
         {
            return null;
         }
      }

      public Span? Union(Span other)
      {
         if(this.Overlaps(other))
         {
            return new Span(Math.Min(this.Start,other.Start), Math.Max(this.End, other.End));
         }
         else
         {
            return null;
         }
      }

      public bool Overlaps(Span other)
      {
         return (this.End >= other.Start && this.Start <= other.End);
      }
   }

   class SpanEqualityComparer: IEqualityComparer<Span>
   {
      public bool Equals(Span? x, Span? y)
      {
         if (x == null || y == null)
         {
            return false;
         }
         return (x.Start == y.Start && x.End == y.End);
      }

      public int GetHashCode(Span obj)
      {
         return obj.GetHashCode();
      }
   }

   public class Program
   {
      public static void Main()
      {
         SpanEqualityComparer comparer = new SpanEqualityComparer();
         List<string> input = new List<string>();
         List<Span[]> pairs = new List<Span[]>();
         string? line;
         while ((line = Console.ReadLine()) != null) {
            var linePairs = new Span[2];
            var rawPairs = line.Split(",",2);
            for(var i = 0; i < 2; i++)
            {
               linePairs[i] = Span.Parse(rawPairs[i]);
            }
            pairs.Add(linePairs);
         }
         int fullyCovered = 0;
         int overlaps = 0;
         foreach(var pair in pairs)
         {
            Span? intersection = pair[0].Intersection(pair[1]);
            if(intersection != null)
            {
               overlaps++;
               if(comparer.Equals(pair[0],intersection)||comparer.Equals(pair[1],intersection))
               {
                  fullyCovered ++;
               }
            }
         }
         Console.WriteLine(String.Format("Fully covered: {0}\nOverlapping: {1}", fullyCovered, overlaps));
      }
   }
}
