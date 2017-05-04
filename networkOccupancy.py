import mdtraj as md
import numpy as np

def distanceOccupancy(traj, startInd, endInd, name,distance,fraction):
        

        allInds = []
	

        
        # Do atom selections, save list with all heavy atoms in sidechains.
        for i in range(startInd,endInd+1):
            choice = "protein and resid " + str(i)# + " and sidechain"
            tmpInd = traj.topology.select(choice)
            allInds.append(tmpInd)
            
        distanceMatrix = np.zeros((len(allInds),len(allInds)))
        time=len(traj.time)

        # Compute distance matrix
        for i in range(0,len(allInds)):
            for j in range(i,len(allInds)):
                #make same residues and nearest neighbors zero
                if i==j:
                    distanceMatrix[i,j]=0
                    distanceMatrix[j,i]=0
                elif i==j-1:
                    distanceMatrix[i,j]=0
                    distanceMatrix[j,i]=0
                else:

                    atomInd1 = allInds[i]
                    atomInd2 = allInds[j]

                    # Get all atom pairs            
                    atom_pairs = np.zeros((len(atomInd1)*len(atomInd2),2))
                    counter = 0
                    for k in range(0,len(atomInd1)):
                        for l in range(0,len(atomInd2)):
                            atom_pairs[counter,0] = atomInd1[k]
                            atom_pairs[counter,1] = atomInd2[l]
                            counter += 1

                    distances = md.compute_distances(traj, atom_pairs,periodic=False)
                    # Find minimum distance between residues and calculate if they are within distance for the fraction of frames
                    pas=0
                    mindist=np.min(distances,axis=1)
                    for m in range(0,len(mindist)):
                        if mindist[m] <= distance:
                            pas += 1
                    if pas/float(time) >= fraction:
                        distanceMatrix[i,j]=1
                        distanceMatrix[j,i]=1
                    else:
                        distanceMatrix[i,j]=0
                        distanceMatrix[j,i]=0
                
        np.savetxt(name+'.txt',distanceMatrix)
        return

def distanceOccupancyOpt(traj, startInd, endInd, name,distance,fraction):
        

        allInds = []
	

        
        # Do atom selections, save list with all heavy atoms in sidechains.
        for i in range(startInd,endInd+1):
            choice = "protein and resid " + str(i)# + " and sidechain"
            tmpInd = traj.topology.select(choice)
            allInds.append(tmpInd)
            
        distanceMatrix = np.zeros((len(allInds),len(allInds)))


        # Compute distance matrix
        for i in range(0,len(allInds)):
            for j in range(i,len(allInds)):
                #make same residues and nearest neighbors zero
                if i==j:
                    distanceMatrix[i,j]=0
                    distanceMatrix[j,i]=0
                elif i==j-1:
                    distanceMatrix[i,j]=0
                    distanceMatrix[j,i]=0
                else:

                    atomInd1 = allInds[i]
                    atomInd2 = allInds[j]

                    # Get all atom pairs            
                    atom_pairs = np.zeros((len(atomInd1)*len(atomInd2),2))
                    counter = 0
                    for k in range(0,len(atomInd1)):
                        for l in range(0,len(atomInd2)):
                            atom_pairs[counter,0] = atomInd1[k]
                            atom_pairs[counter,1] = atomInd2[l]
                            counter += 1

                    distances = md.compute_distances(traj, atom_pairs,periodic=False)
                    # Find minimum distance between residues and calculate if they are within distance for the fraction of frames
                    pas=0
                    mindist=np.min(distances,axis=1)
                    test=np.mean(mindist <= distance)
                    if test >= fraction:
                        distanceMatrix[i,j]=1
                        distanceMatrix[j,i]=1
                    else:
                        distanceMatrix[i,j]=0
                        distanceMatrix[j,i]=0
                
        np.savetxt(name+'.txt',distanceMatrix)
        return

#from networkOccupancy import *
#import mdtraj as md
#import numpy as np

#traj = md.load('../EAGplusCaCaM_100ps_pro.dcd', top='../EAGplusCaCam_pro.psf')
#distanceOccupancyOpt(traj, 0, 3419, "contact_matrix_10_correctOpt", 1, .75)
