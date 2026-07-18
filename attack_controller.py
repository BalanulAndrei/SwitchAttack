#!/usr/bin/env python3

from pathlib import Path
from subprocess import STDOUT

import topology


PROJECT_DIR = Path(__file__).resolve().parent

attack_processes = {}
attack_log_files = {}
attack_log_paths = {}


def get_host(host_name):
	host_names = [host.name for host in topology.hosts]

	if host_name not in host_names:
		raise ValueError(f"Host does not exist: {host_name}")

	return topology.net.get(host_name)


def stop_attack(attack_name):
	process = attack_processes.get(attack_name)

	if process is not None and process.poll() is None:
		process.terminate()

	attack_processes.pop(attack_name, None)

	log_file = attack_log_files.pop(attack_name, None)

	if log_file is not None:
		log_file.close()


def start_mac_flood(attacker_name, count=100, interval=0.01):
	stop_attack("mac_flood")

	attacker = get_host(attacker_name)
	attacker_interface = attacker.defaultIntf().name

	log_path = f"/tmp/mac_flood_{attacker_name}.log"
	log_file = open(log_path, "w")

	code = (
		"from attacks.mac_flood import run_mac_flood; "
		f"run_mac_flood("
		f"interface={attacker_interface!r}, "
		f"destination_mac='ff:ff:ff:ff:ff:ff', "
		f"count={count}, "
		f"interval={interval}"
		f")"
	)

	process = attacker.popen(
		["python3", "-u", "-c", code],
		stdout=log_file,
		stderr=STDOUT,
		cwd=str(PROJECT_DIR)
	)

	attack_processes["mac_flood"] = process
	attack_log_files["mac_flood"] = log_file
	attack_log_paths["mac_flood"] = log_path

	return log_path


def start_pod(attacker_name, victim_name, interval=0.01):
	stop_attack("pod")

	attacker = get_host(attacker_name)
	victim = get_host(victim_name)

	log_path = f"/tmp/pod_{attacker_name}_to_{victim_name}.log"
	log_file = open(log_path, "w")

	code = (
		"from attacks.pod import run_pod; "
		f"run_pod("
		f"attacker_ip={attacker.IP()!r}, "
		f"destination_ip={victim.IP()!r}, "
		f"interval={interval}"
		f")"
	)

	process = attacker.popen(
		["python3", "-u", "-c", code],
		stdout=log_file,
		stderr=STDOUT,
		cwd=str(PROJECT_DIR)
	)

	attack_processes["pod"] = process
	attack_log_files["pod"] = log_file
	attack_log_paths["pod"] = log_path

	return log_path


def read_attack_log(attack_name):
	log_path = attack_log_paths.get(attack_name)

	if log_path is None:
		return "No log found."

	try:
		with open(log_path, "r") as file:
			return file.read()
	except FileNotFoundError:
		return "Log file not found."


def stop_all_attacks():
	for attack_name in list(attack_processes.keys()):
		stop_attack(attack_name)