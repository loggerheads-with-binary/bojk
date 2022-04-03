#![windows_subsystem = "windows"]

use std::process::Command;
use std::env ;

use std::fs;
use std::path::PathBuf;

static EXECUTABLE_PATH : &'static str = r"C:\Users\hp\AppData\Local\atom\atom.exe";

fn main() -> () {

	let args: Vec<String> = env::args().collect();

	if args.len() == 1 {
		return;
	}

	let FilePath = fs::canonicalize(PathBuf::from(&args[1])).expect("Canonicalization Failed");

	Command::new(EXECUTABLE_PATH).arg(&FilePath).spawn().expect("Text Editor call failed");
}
