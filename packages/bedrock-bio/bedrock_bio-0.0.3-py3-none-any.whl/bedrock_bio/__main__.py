
import click
from typing import Literal, Optional

from bedrock_bio.models.boltz1.main import predict as boltz1

@click.group()
def cli():
    print('CLI')


@cli.group()
def run():
    print('RUN')


run.add_command(boltz1)




@run.command()
def alphafold2():
    print('ALPHAFOLD2')


@run.command()
def esm2():
    print('ESM2')


@run.command()
def esm3():
    print('ESM3')


@run.command()
def evo2():
    print('EVO2')


@run.command()
def evodiff():
    print('EVODIFF')


@run.command()
def ligand_mpnn():
    print('LIGAND-MPNN')


@run.command()
def openfold2():
    print('OPENFOLD2')


@run.command()
def progen2():
    print('PROGEN2')


@run.command()
def protein_mpnn():
    print('PROTEIN-MPNN')


@run.command()
def rfantibody():
    print('RFANTIBODY')


@run.command()
def rfdiffusion():
    print('RFDIFFUSION')


@run.command()
def rfdiffusion_all_atom():
    print('RFDIFFUSION-ALL-ATOM')


if __name__ == '__main__':
    cli()

