﻿/*
Copyright 2015-2022 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
Under the terms of Contract DE-NA0003525 with NTESS, the U.S.Government retains certain
rights in this software.

You should have received a copy of the GNU General Public License along with
HyRAM+. If not, see https://www.gnu.org/licenses/.
*/

using System;
using System.Threading.Tasks;
using System.Windows.Forms;


namespace SandiaNationalLaboratories.Hyram
{
    public partial class PlumeForm : UserControl
    {
        private string _plotFilename; // result
        private bool _analysisStatus;
        private string _statusMsg;
        private string _warningMsg;
        private float _mass_flow_rate;

        public PlumeForm()
        {
            InitializeComponent();
        }

        private void CpGasPlumeDispersion_Load(object sender, EventArgs e)
        {
            spinnerPictureBox.Hide();
            CheckFormValid();

            // Populate notional nozzle model combo box. Manual to exclude Harstad
            nozzleSelector.DataSource = StateContainer.Instance.NozzleModels;
            nozzleSelector.SelectedItem = StateContainer.GetValue<NozzleModel>("NozzleModel");

            fuelPhaseSelector.DataSource = StateContainer.Instance.FluidPhases;
            fuelPhaseSelector.SelectedItem = StateContainer.Instance.GetFluidPhase();

            StateContainer.Instance.FuelTypeChangedEvent += delegate { RefreshGridParameters(); };

            RefreshGridParameters();
        }

        private void RefreshGridParameters()
        {
            plumeInputGrid.Rows.Clear();

            // Create collection initially containing common params
            ParameterWrapperCollection formParams = new ParameterWrapperCollection(new[]
            {
                new ParameterWrapper("PlumeWrapper.XMin", "X lower limit", DistanceUnit.Meter,
                    StockConverters.DistanceConverter),
                new ParameterWrapper("PlumeWrapper.XMax", "X upper limit", DistanceUnit.Meter,
                    StockConverters.DistanceConverter),
                new ParameterWrapper("PlumeWrapper.YMin", "Y lower limit", DistanceUnit.Meter,
                    StockConverters.DistanceConverter),
                new ParameterWrapper("PlumeWrapper.YMax", "Y upper limit", DistanceUnit.Meter,
                    StockConverters.DistanceConverter),
                new ParameterWrapper("PlumeWrapper.Contours", "Contours (mole fraction)", UnitlessUnit.Unitless,
                    StockConverters.UnitlessConverter),

                new ParameterWrapper("ambientPressure", "Ambient pressure", PressureUnit.Pa,
                    StockConverters.PressureConverter),
                new ParameterWrapper("ambientTemperature", "Ambient temperature", TempUnit.Kelvin,
                    StockConverters.TemperatureConverter),
                new ParameterWrapper("orificeDiameter", "Orifice diameter", DistanceUnit.Meter,
                    StockConverters.DistanceConverter),
                new ParameterWrapper("orificeDischargeCoefficient", "Orifice discharge coefficient", UnitlessUnit.Unitless,
                    StockConverters.UnitlessConverter),
                new ParameterWrapper("PlumeWrapper.jet_angle", "Angle of jet", AngleUnit.Radians,
                    StockConverters.AngleConverter)
            });;

            formParams.Add("fluidPressure",
                new ParameterWrapper("fluidPressure", "Fluid pressure (absolute)", PressureUnit.Pa,
                    StockConverters.PressureConverter));

            if (FluidPhase.DisplayTemperature())
            {
                formParams.Add("fluidTemperature",
                    new ParameterWrapper("fluidTemperature", "Fluid temperature", TempUnit.Kelvin,
                        StockConverters.TemperatureConverter));
            }

            StaticGridHelperRoutines.InitInteractiveGrid(plumeInputGrid, formParams, false);

            plumeInputGrid.Columns[0].Width = 200;
            plumeInputGrid.Columns[1].Width = 200;
            plumeInputGrid.Columns[2].Width = 200;

            CheckFormValid();
        }

        private void CheckFormValid()
        {
            bool showWarning = false;
            string warningText = "";

            // if liquid, validate fuel pressure
            if (!StateContainer.ReleasePressureIsValid())
            {
                warningText = MessageContainer.GetAlertMessageReleasePressureInvalid();
                showWarning = true;
            }

            inputWarning.Text = warningText;
            inputWarning.Visible = showWarning;
            executeButton.Enabled = !showWarning;
        }

        private void Execute()
        {
            var ambPres= StateContainer.GetNdValue("ambientPressure", PressureUnit.Pa);
            var ambTemp = StateContainer.GetNdValue("ambientTemperature", TempUnit.Kelvin);
            var relPres = StateContainer.GetNdValue("fluidPressure", PressureUnit.Pa);
            var relTemp = StateContainer.GetNdValue("fluidTemperature", TempUnit.Kelvin);
            var relAngle = StateContainer.GetNdValue("PlumeWrapper.jet_angle", AngleUnit.Radians);

            var orifDiam = StateContainer.GetNdValue("orificeDiameter", DistanceUnit.Meter);
            var disCoeff = StateContainer.GetNdValue("orificeDischargeCoefficient", UnitlessUnit.Unitless);

            var xMin = StateContainer.GetNdValue("PlumeWrapper.XMin", DistanceUnit.Meter);
            var xMax = StateContainer.GetNdValue("PlumeWrapper.XMax", DistanceUnit.Meter);
            var yMin = StateContainer.GetNdValue("PlumeWrapper.YMin", DistanceUnit.Meter);
            var yMax = StateContainer.GetNdValue("PlumeWrapper.YMax", DistanceUnit.Meter);

            var contours = StateContainer.GetNdValue("PlumeWrapper.Contours", UnitlessUnit.Unitless);
            var nozzleModel = StateContainer.GetValue<NozzleModel>("NozzleModel");
            var plotTitle = StateContainer.GetValue<string>("PlumeWrapper.PlotTitle");

            var physInt = new PhysicsInterface();
            _analysisStatus = physInt.CreatePlumePlot(
                ambPres, ambTemp,
                relPres, relTemp, relAngle,
                orifDiam, disCoeff,
                xMin, xMax, yMin, yMax,
                contours, nozzleModel.GetKey(), plotTitle,
                out _statusMsg, out _warningMsg, out _plotFilename, out _mass_flow_rate);
        }

        private void DisplayResults()
        {
            spinnerPictureBox.Hide();
            executeButton.Enabled = true;

            if (!_analysisStatus)
            {
                MessageBox.Show(_statusMsg);
            }
            else
            {
                outputPictureBox.Load(_plotFilename);
                mainTabControl.SelectedTab = outputTab;
                outputMassFlowRate.Text = _mass_flow_rate.ToString("E3");

                if (_warningMsg.Length != 0)
                {
                    outputWarning.Text = _warningMsg;
                    outputWarning.Show();
                }
            }
        }

        private void plumeInputGrid_CellValueChanged(object sender, DataGridViewCellEventArgs e)
        {
            StaticGridHelperRoutines.ProcessDataGridViewRowValueChangedEvent((DataGridView) sender, e, 1, 2, false);
            CheckFormValid();
        }

        private async void calculateButton_Click(object sender, EventArgs e)
        {
            spinnerPictureBox.Show();
            outputWarning.Hide();
            executeButton.Enabled = false;
            await Task.Run(() => Execute());
            DisplayResults();
        }

        private void tbPlotTitle_TextChanged(object sender, EventArgs e)
        {
            if (tbPlotTitle.Text != null)
                StateContainer.SetValue("PlumeWrapper.PlotTitle", tbPlotTitle.Text);
            else
                StateContainer.SetValue("PlumeWrapper.PlotTitle", "");
        }

        private void nozzleSelector_SelectionChangeCommitted(object sender, EventArgs e)
        {
            var modelName = nozzleSelector.SelectedItem.ToString();
            StateContainer.SetValue("NozzleModel", NozzleModel.ParseNozzleModelName(modelName));
        }

        private void fuelPhaseSelector_SelectionChangeCommitted(object sender, EventArgs e)
        {
            StateContainer.SetReleasePhase((FluidPhase)fuelPhaseSelector.SelectedItem);
            RefreshGridParameters();
        }

    }
}