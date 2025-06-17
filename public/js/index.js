let clusterTable;
let birdDataTable;

// what the clusters actually look like
// are the things we expect to be clustered actually clustered (e.g., winter ducks, migratory thrushes)
// what are the clusters we don't know why they're clustering? prob a data thing (e.g., very sparse)

function preload() {
  const dataFolder = '../data/processed';

  const clusterFilename = 'bci_hotspot-abundance.csv';
  const dataFilename = 'hotspot_L199454_trimmed.tsv';

  clusterTable = loadTable(
    `${dataFolder}/${clusterFilename}`,
    'csv',
    'header',
    onClusterTableLoad
  );

  birdDataTable = loadTable(
    `${dataFolder}/${dataFilename}`,
    'tsv',
    'header',
    onBirdDataLoad
  );
}

function onClusterTableLoad(data) {
  console.debug({ clusterData: data });
}

function onBirdDataLoad(data) {
  console.debug({ birdData: data });
}

function setup() {
  console.debug('settings up!');

  createCanvas(200, 200);
  background('orange');

  // ebird codes
  drawClusters()
}

function drawClusters() {
  console.debug(clusterTable.getRows())
  for (let index = 0; index < clusterTable.getRowCount(); index += 1) {
    console.debug(clusterTable.getRow(index))
  }
}



// [...new Array(12)].map((_, index) => new Intl.DateTimeFormat("en-US", { month: "short"} ).format(new Date(2025, index))).flatMap(mon => [...new Array(4)].map((_, wI) => `${mon}${wI}`)).join(',')
