using Spring_diogram.DATA;
using System.Globalization;
using System.IO;
using System.Text.Json;

namespace Spring_diogram.Parsers
{
    public class RcParser : ParserBase
    {
        public RcParser(string path) : base(path) { }

        public override InputData Parse()
        {
            var input = new RCInput();

            try
            {
                // Парсинг JSON формата
                string jsonContent = File.ReadAllText(_path);
                using JsonDocument doc = JsonDocument.Parse(jsonContent);
                JsonElement root = doc.RootElement;

                // Чтение полей из JSON
                if (root.TryGetProperty("Resistance", out JsonElement resistanceElem) ||
                    root.TryGetProperty("resistance", out resistanceElem))
                {
                    if (resistanceElem.TryGetDouble(out double resistance))
                        input.Resistance = resistance;
                }

                if (root.TryGetProperty("Capacitance", out JsonElement capacitanceElem) ||
                    root.TryGetProperty("capacitance", out capacitanceElem))
                {
                    if (capacitanceElem.TryGetDouble(out double capacitance))
                        input.Capacitance = capacitance;
                }

                if (root.TryGetProperty("VoltageSource", out JsonElement voltageSourceElem) ||
                    root.TryGetProperty("voltageSource", out voltageSourceElem) ||
                    root.TryGetProperty("voltagesource", out voltageSourceElem))
                {
                    if (voltageSourceElem.TryGetDouble(out double voltageSource))
                        input.VoltageSource = voltageSource;
                }

                if (root.TryGetProperty("U0", out JsonElement u0Elem) ||
                    root.TryGetProperty("u0", out u0Elem))
                {
                    if (u0Elem.TryGetDouble(out double u0))
                        input.U0 = u0;
                }

                if (root.TryGetProperty("TimeMax", out JsonElement timeMaxElem) ||
                    root.TryGetProperty("timemax", out timeMaxElem))
                {
                    if (timeMaxElem.TryGetDouble(out double timeMax))
                        input.MaxTime = timeMax;
                }

                if (root.TryGetProperty("TimeStep", out JsonElement timeStepElem) ||
                    root.TryGetProperty("timestep", out timeStepElem))
                {
                    if (timeStepElem.TryGetDouble(out double timeStep))
                        input.DeltaT = timeStep;
                }

                input.Name = "RC Circuit";
                return input;
            }
            catch (Exception ex)
            {
                throw new Exception($"Ошибка парсинга RC файла (JSON): {ex.Message}", ex);
            }
        }
    }
}

