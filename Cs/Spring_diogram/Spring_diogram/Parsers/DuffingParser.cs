using Spring_diogram.DATA;
using System.Globalization;
using System.IO;

namespace Spring_diogram.Parsers
{
    public class DuffingParser : ParserBase
    {
        public DuffingParser(string path) : base(path) { }

        public override InputData Parse()
        {
            var input = new DuffingInput();

            try
            {
                string[] lines = File.ReadAllLines(_path);

                // Формат файла duffer.txt:
                // Строка 1: "duffer" (название формата)
                // Строка 2: заголовки столбцов (delta, alpha, beta, ...)
                // Строка 3: значения
                if (lines.Length < 3)
                    throw new FormatException("Файл должен содержать как минимум три строки: название формата, заголовки и значения");

                // Пропускаем первую строку (название формата), читаем заголовки со второй строки
                string[] headers = lines[1].Split(new[] { '\t', ';', ',' }, StringSplitOptions.RemoveEmptyEntries);
                string[] values = lines[2].Split(new[] { '\t', ';', ',' }, StringSplitOptions.RemoveEmptyEntries);

                if (headers.Length != values.Length)
                    throw new FormatException("Количество заголовков не совпадает с количеством значений");

                for (int i = 0; i < headers.Length; i++)
                {
                    string header = headers[i].Trim().ToLower();
                    string value = values[i].Trim();

                    if (!double.TryParse(value, NumberStyles.Any, CultureInfo.InvariantCulture, out double numericValue))
                        continue;

                    switch (header)
                    {
                        case "delta":
                            input.Delta = numericValue;
                            break;
                        case "alpha":
                            input.Alpha = numericValue;
                            break;
                        case "beta":
                            input.Beta = numericValue;
                            break;
                        case "gamma":
                            input.Gamma = numericValue;
                            break;
                        case "omega":
                            input.Omega = numericValue;
                            break;
                        case "x0":
                            input.X0 = numericValue;
                            break;
                        case "v0":
                            input.V0 = numericValue;
                            break;
                        case "skiptransient":
                        case "skip_transient":
                            input.SkipTransient = numericValue;
                            break;
                        case "recordstride":
                        case "record_stride":
                            input.RecordStride = int.Parse(value, CultureInfo.InvariantCulture);
                            break;
                        case "maxtime":
                        case "time_max":
                        case "timemax":
                            input.MaxTime = numericValue;
                            break;
                        case "dt":
                        case "timestep":
                        case "time_step":
                        case "deltat":
                            input.DeltaT = numericValue;
                            break;
                    }
                }

                input.Name = "Duffing";
                return input;
            }
            catch (FormatException ex)
            {
                throw new FormatException($"Ошибка формата файла Дуффинга: {ex.Message}", ex);
            }
            catch (IOException ex)
            {
                throw new IOException($"Ошибка чтения файла Дуффинга: {ex.Message}", ex);
            }
        }
    }
}
