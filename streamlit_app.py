<?php
// Web Keuangan Sederhana - Warkop Tjahaja Abadi
// Simpan file ini sebagai index.php
// Database MySQL:
// CREATE DATABASE keuangan_warkop;
// USE keuangan_warkop;
// CREATE TABLE transaksi (
//   id INT AUTO_INCREMENT PRIMARY KEY,
//   tanggal DATE NOT NULL,
//   jenis ENUM('Pemasukan','Pengeluaran') NOT NULL,
//   keterangan VARCHAR(255) NOT NULL,
//   nominal DECIMAL(10,2) NOT NULL
// );

$conn = new mysqli('localhost', 'root', '', 'keuangan_warkop');
if ($conn->connect_error) {
    die('Koneksi gagal: ' . $conn->connect_error);
}

// Tambah transaksi
if (isset($_POST['simpan'])) {
    $tanggal = $_POST['tanggal'];
    $jenis = $_POST['jenis'];
    $keterangan = $_POST['keterangan'];
    $nominal = $_POST['nominal'];

    $sql = "INSERT INTO transaksi (tanggal, jenis, keterangan, nominal)
            VALUES ('$tanggal', '$jenis', '$keterangan', '$nominal')";
    $conn->query($sql);
    header('Location: index.php');
}

// Ambil data transaksi
$data = $conn->query('SELECT * FROM transaksi ORDER BY tanggal DESC');

// Hitung total pemasukan
$pemasukan = $conn->query("SELECT SUM(nominal) as total FROM transaksi WHERE jenis='Pemasukan'")->fetch_assoc()['total'] ?? 0;

// Hitung total pengeluaran
$pengeluaran = $conn->query("SELECT SUM(nominal) as total FROM transaksi WHERE jenis='Pengeluaran'")->fetch_assoc()['total'] ?? 0;

$saldo = $pemasukan - $pengeluaran;
?>

<!DOCTYPE html>
<html>
<head>
    <title>Sistem Keuangan Warkop</title>
    <style>
        body { font-family: Arial; margin: 30px; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        table, th, td { border: 1px solid black; padding: 8px; }
        input, select { padding: 8px; margin: 5px; }
        .box { padding: 10px; margin: 10px 0; border: 1px solid #ccc; }
    </style>
</head>
<body>

<h2>Web Keuangan Warkop Tjahaja Abadi</h2>

<div class="box">
    <h3>Dashboard</h3>
    <p>Total Pemasukan: Rp <?= number_format($pemasukan,0,',','.') ?></p>
    <p>Total Pengeluaran: Rp <?= number_format($pengeluaran,0,',','.') ?></p>
    <p>Saldo Akhir: Rp <?= number_format($saldo,0,',','.') ?></p>
</div>

<h3>Tambah Transaksi</h3>
<form method="POST">
    <input type="date" name="tanggal" required>
    <select name="jenis" required>
        <option value="Pemasukan">Pemasukan</option>
        <option value="Pengeluaran">Pengeluaran</option>
    </select>
    <input type="text" name="keterangan" placeholder="Keterangan" required>
    <input type="number" name="nominal" placeholder="Nominal" required>
    <button type="submit" name="simpan">Simpan</button>
</form>

<h3>Riwayat Transaksi</h3>
<table>
    <tr>
        <th>Tanggal</th>
        <th>Jenis</th>
        <th>Keterangan</th>
        <th>Nominal</th>
    </tr>
    <?php while($row = $data->fetch_assoc()) { ?>
    <tr>
        <td><?= $row['tanggal'] ?></td>
        <td><?= $row['jenis'] ?></td>
        <td><?= $row['keterangan'] ?></td>
        <td>Rp <?= number_format($row['nominal'],0,',','.') ?></td>
    </tr>
    <?php } ?>
</table>

</body>
</html>
