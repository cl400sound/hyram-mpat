﻿/*
Copyright 2015-2022 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
Under the terms of Contract DE-NA0003525 with NTESS, the U.S.Government retains certain
rights in this software.

You should have received a copy of the GNU General Public License along with
HyRAM+. If not, see https://www.gnu.org/licenses/.
*/

using System.Windows.Forms;

namespace SandiaNationalLaboratories.Hyram
{
    public class AnalysisForm : UserControl
    {
        public string AlertMessage { get; set; } = "";
        public int AlertType { get; set; } = 0;
        public bool AlertDisplayed { get; set; } = false;

        protected MainForm MainForm;

        public virtual void CheckFormValid()
        {
        }

        public virtual void OnFormDisplay()
        {
        }
    }
}
