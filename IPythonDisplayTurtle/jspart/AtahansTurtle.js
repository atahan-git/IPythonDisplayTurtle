
var turtle = drawTurtle("#00A651","#FFF600");

console.log(actionData)
console.log(actionData.length);
// The points data is injected by the python library
// it is an array with these elements:
// [0-rotation:int, 1-positionX:int, 2-positionY:int
//  3-speed:1-10, 4-rotspeed:1-10, 
//  5-penDown:1/0, 6-penColor:string, 7-penWidth:int, 
//  8-turtleMainColor:string, 9-turtleAccentColor:string, 10-backgroundColor:string, ]
// total 11 items

var movDestination = new Point(actionData[0][1], actionData[0][2]);
var movVector = movDestination - turtle.position;
turtle.position = movDestination;

var rotDestination = actionData[0][0];
var curRotation = rotDestination;
var defRotation = rotDestination;

var speed = 1.0;
var rotSpeed = 1.0;

var path = null;
var isGoing = true;
var movOrRotate = true;
var n = 0;

processActionData(0);
SetAnimStates();
function onFrame(event) {
	if(event.count < 60){
		return;
	}
	
	wiggleTurtle(event.count, isGoing);
	
	if(isGoing){
		if(movOrRotate){
			// Each frame, move the path 1/30th of the difference in position
			// between it and the destination.

			// The vector is the difference between the position of
			// the text item and the destination point:

			// We add 1/30th of the vector to the position property
			// of the text item, to move it in the direction of the
			// destination point:
			var distance = (movDestination - turtle.position).length;
			var isArrived = false;
			if(distance>speed){
				turtle.position += movVector.normalize(speed);
			}else{
				turtle.position = movDestination
				isArrived = true;
			}
			console.log("turtle moving to: " + movDestination.toString())
			if(path != null){
				path.lastSegment.point = turtle.position;
			}

			// If the distance between the path and the destination is less
			// than 5, we define a new random point in the view to move the
			// path to:
			if (isArrived) {
				n = n + 1;
				if (n >= actionData.length){
					isGoing = false;
					return;
				}
				
				movDestination = new Point(actionData[n][1], actionData[n][2]);
				movVector = movDestination - turtle.position;
				rotDestination = actionData[n][0];
				
				processActionData(n);
				
				// Death Check
				if (typeof losePlaces !== 'undefined') {
					for(var i = 0; i < losePlaces.length; i++){
						var distance = (losePlaces[i] - turtle.position).length;
						if(distance < 1){
							console.log("snake Died!");
							Die();
							isGoing = false;
						}
					}
				}
				
				// Win Check
				if (typeof winPlace !== 'undefined') {
					var distance = (winPlace - turtle.position).length;
					if(distance < 1){
						console.log("You won!");
						Win();
						isGoing = false;
					}
					
				}
				
				console.log(actionData[n])
				if(actionData[n-1][0] == actionData[n][0]){
					movOrRotate = true;
				}else{
					movOrRotate = false;
				}
				
				
			}
		}else{
			var distance = (rotDestination - curRotation)
			var isArrived = false;
			if(distance>rotspeed){
				rotDelta = distance > 0 ? rotspeed : -rotspeed;
				turtle.rotate(rotDelta);
				curRotation += rotDelta;
			}else{
				turtle.rotate(distance);
				curRotation += distance;
				isArrived = true;
			}
			console.log("turtle rotating to: " + rotDestination.toString())
			
			if(isArrived){
				n = n + 1;
				if (n >= actionData.length){
					isGoing = false;
					return;
				}
				
				movDestination = new Point(actionData[n][1], actionData[n][2]);
				movVector = movDestination - turtle.position;
				rotDestination = actionData[n][0];
				
				processActionData(n);
				
				if(actionData[n-1][0] == actionData[n][0]){
					movOrRotate = true;
				}else{
					movOrRotate = false;
				}
			}
		}
	}
}

function Die (){
	
	var box = new Path.Rectangle({
		point: [100-10, 100-25-10],
		size: [210, 35+10+10],
		fillColor: '#ffc4c4',
		strokeColor: 'red'
	});
	
	var text = new PointText({
		point: [100, 100],
		content: 'Your snake died!',
		fillColor: 'black',
		fontFamily: 'Courier New',
		fontWeight: 'bold',
		fontSize: 25
	});
}

function Win (){
	
	var box = new Path.Rectangle({
		point: [150	-10, 100-25-10],
		size: [135, 35+10+10],
		fillColor: '#c6ffc4',
		strokeColor: 'green'
	});
	
	var text = new PointText({
		point: [150, 100],
		content: 'You Won!',
		fillColor: 'black',
		fontFamily: 'Courier New',
		fontWeight: 'bold',
		fontSize: 25
	});
}

function processActionData (n){
	setSpeed(n);
	setPenInfo(n);
}


function setSpeed (n){
	speed = actionData[n][3] / 10.0;
	rotspeed = actionData[n][4] / 5.0;
}

function setPenInfo (n){
	if(actionData[n][5] == 1){
		path = new Path({
			// 80% black:
			strokeColor: actionData[n][6],
			strokeWidth: actionData[n][7],
			strokeCap: 'round'
		});
		path.add(turtle.position, turtle.position)
	}else{
		path = null
	}
}



function drawTurtle (mainColor, accentColor){
	// pixel size = 600x150
	//var sizeMultiplier = 0.1;
	//var xOffset = -(800 + 600/2);
	//var yOffset = -(375 + 150/2);
	/* For the numbers I used an image program to draw and used this python code to convert the pixel coordinates to more reasonable numbers
	def x(num):
		print((num-1100)*0.1)
	
	def y(num):
		print((num-450)*0.1)
	*/
	
	var tongue1 = new Path.Line({from:[26,-1.6], to:[35.5,-1.6], strokeWidth:2, strokeColor:'red', strokeCap:'round'});
	var tongue2 = new Path.Line({from:[35.5,-1.6], to:[37.4,0.1], strokeWidth:2, strokeColor:'red', strokeCap:'round'});
	var tongue3 = new Path.Line({from:[35.5,-1.6], to:[37.4,-3.3], strokeWidth:2, strokeColor:'red', strokeCap:'round'});
	
	
	var segment0 = new Path.Rectangle(new Rectangle(new Point (-29.2, -1.8), new Point(-16.9, 2.1)), new Size(2,2));
	segment0.fillColor = mainColor;
	
	var segment1 = new Path.Rectangle(new Rectangle(new Point (-23.1, -4.8), new Point(-5.5, 0.1)), new Size(3,3));
	segment1.fillColor = mainColor;
	
	var segment2 = new Path.Rectangle(new Rectangle(new Point (-12.2, -2.3), new Point(15.5, 7.7)), new Size(5,5));
	segment2.fillColor = mainColor;
	
	var segment3 = new Path.Rectangle(new Rectangle(new Point (7.0, -7.4), new Point(30.5, 3.4)), new Size(5,5));
	segment3.fillColor = mainColor;
	
	
	var spot1 = new Path.Arc({from: [10.9, -7.6], through: [14.4, -2.8], to: [18.2, -7.6], fillColor: accentColor});
	var spot2 = new Path.Arc({from: [3.9, 7.9], through: [7.3, 3.4], to: [11.3, 7.9], fillColor: accentColor});
	var spot3 = new Path.Arc({from: [-5.7, -2.4], through: [-2.7, 2.2], to: [1.5, -2.4], fillColor: accentColor});
	var spot4 = new Path.Arc({from: [-21.5, 2.3], through: [-18.2, -2.0], to: [-14.8, 0.3], fillColor: accentColor});
	spot4.add(new Point(-16.8, 0.3));
	spot4.add(new Point(-16.8, 1.0));
	spot4.add(new Point(-18.1, 2.2));
	
	var eye1 = new Path.Circle({center: [22.5, -5.9], radius: 3});
	eye1.fillColor = 'black'
	var eyeSparkBig1 = new Path.Circle({center: [23.3, -7.2], radius: 1});
	eyeSparkBig1.fillColor = 'white'
	var eyeSparkSmall1 = new Path.Circle({center: [20.9, -5.9], radius: 0.6});
	eyeSparkSmall1.fillColor = 'white'
	
	var eye2 = new Path.Circle({center: [22.5, 2.9], radius: 3});
	eye2.fillColor = 'black'
	var eyeSparkBig2 = new Path.Circle({center: [23.3, 1.6], radius: 1});
	eyeSparkBig2.fillColor = 'white'
	var eyeSparkSmall2 = new Path.Circle({center: [20.9, 2.9], radius: 0.6});
	eyeSparkSmall2.fillColor = 'white'
	
	var turtle = new Group([tongue1, tongue2, tongue3, segment0, segment1, segment2, segment3, eye1, eyeSparkBig1, eyeSparkSmall1, eye2, eyeSparkBig2, eyeSparkSmall2, spot1, spot2, spot3, spot4])
	turtle.scale(0.8);
	return turtle;
}

function SetAnimStates (){
	// set default position and animated position of everything
	tongue1Anim = AnimStateMaker(0, new Point(-12,0));
	tongue2Anim = AnimStateMaker(1, new Point(-12,0));
	tongue3Anim = AnimStateMaker(2, new Point(-12,0));


	segment0Anim = AnimStateMaker(3, new Point(0, -2));
	segment0AnimDecal = AnimStateMaker(16, new Point(0, -2));

	segment1Anim = AnimStateMaker(4, new Point(0, 2));

	segment2Anim = AnimStateMaker(5, new Point(0, -4));
	segment2AnimDecal0 = AnimStateMaker(15, new Point(0, -4));
	segment2AnimDecal1 = AnimStateMaker(14, new Point(0, -4));

	p3 = new Point(0, 2);
	segment3Anim = AnimStateMaker(6, p3);
	segment3AnimDecal0 = AnimStateMaker(13, p3);
	segment3AnimDecal1 = AnimStateMaker(12, p3);
	segment3AnimDecal2 = AnimStateMaker(11, p3);
	segment3AnimDecal3 = AnimStateMaker(10, p3);
	segment3AnimDecal4 = AnimStateMaker(9, p3);
	segment3AnimDecal5 = AnimStateMaker(8, p3);
	segment3AnimDecal6 = AnimStateMaker(7, p3);
}

var framesUntilDefaultState = 0;
var isFirstTime = true;
function wiggleTurtle(animState, isMoving){
	var bodyAnimLength = 120;
	var tongueAnimLength = 180;
	var tongueState = animState%tongueAnimLength;
	var bodyAnimState = animState%bodyAnimLength;
	
	AnimatePart(0, tongueState, tongueAnimLength, tongue1Anim);
	AnimatePart(1, tongueState, tongueAnimLength, tongue2Anim);
	AnimatePart(2, tongueState, tongueAnimLength, tongue3Anim);
		
	if(isMoving){
		AnimatePart(3, bodyAnimState, bodyAnimLength, segment0Anim);
		AnimatePart(16, bodyAnimState, bodyAnimLength, segment0AnimDecal);
		
		AnimatePart(4, bodyAnimState, bodyAnimLength, segment1Anim);
		
		AnimatePart(5, bodyAnimState, bodyAnimLength, segment2Anim);
		AnimatePart(15, bodyAnimState, bodyAnimLength, segment2AnimDecal0);
		AnimatePart(14, bodyAnimState, bodyAnimLength, segment2AnimDecal1);
		
		/*AnimatePart(6, bodyAnimState, bodyAnimLength, segment3Anim);
		AnimatePart(13, bodyAnimState, bodyAnimLength, segment3AnimDecal0);
		AnimatePart(12, bodyAnimState, bodyAnimLength, segment3AnimDecal1);
		AnimatePart(11, bodyAnimState, bodyAnimLength, segment3AnimDecal2);
		AnimatePart(10, bodyAnimState, bodyAnimLength, segment3AnimDecal3);
		AnimatePart(9, bodyAnimState, bodyAnimLength, segment3AnimDecal4);
		AnimatePart(8, bodyAnimState, bodyAnimLength, segment3AnimDecal5);
		AnimatePart(7, bodyAnimState, bodyAnimLength, segment3AnimDecal6);*/
	}else{
		if(isFirstTime){
			framesUntilDefaultState = bodyAnimLength-bodyAnimState + (bodyAnimLength/2);
			framesUntilDefaultState %= bodyAnimLength;
			isFirstTime = false;
		}
		
		if(framesUntilDefaultState>0){
			AnimatePart(3, bodyAnimState, bodyAnimLength, segment0Anim);
			AnimatePart(16, bodyAnimState, bodyAnimLength, segment0AnimDecal);
			
			AnimatePart(4, bodyAnimState, bodyAnimLength, segment1Anim);
			
			AnimatePart(5, bodyAnimState, bodyAnimLength, segment2Anim);
			AnimatePart(15, bodyAnimState, bodyAnimLength, segment2AnimDecal0);
			AnimatePart(14, bodyAnimState, bodyAnimLength, segment2AnimDecal1);
			
			/*AnimatePart(6, bodyAnimState, bodyAnimLength, segment3Anim);
			AnimatePart(13, bodyAnimState, bodyAnimLength, segment3AnimDecal0);
			AnimatePart(12, bodyAnimState, bodyAnimLength, segment3AnimDecal1);
			AnimatePart(11, bodyAnimState, bodyAnimLength, segment3AnimDecal2);
			AnimatePart(10, bodyAnimState, bodyAnimLength, segment3AnimDecal3);
			AnimatePart(9, bodyAnimState, bodyAnimLength, segment3AnimDecal4);
			AnimatePart(8, bodyAnimState, bodyAnimLength, segment3AnimDecal5);
			AnimatePart(7, bodyAnimState, bodyAnimLength, segment3AnimDecal6);*/
			framesUntilDefaultState -= 1;
		}
	}
}

function AnimStateMaker (id, offset){
	//return [turtle.children[id].position, turtle.children[id].position + offset];
	return offset;
}

function AnimatePart (id, animState, animLength, anim){
	if(animState<(animLength/2)){
		var vector = -anim;
		vector /= (animLength/2);
		vector.angle += (curRotation-defRotation);
		turtle.children[id].translate(vector)
		//turtle.children[id].position = lerp(anim[0], anim[1], animState/(animLength/2));
	}else{
		var vector = anim;
		vector /= (animLength/2);
		vector.angle += (curRotation-defRotation);
		turtle.children[id].translate(vector)
		//turtle.children[id].position = lerp(anim[0], anim[1], (animLength-animState)/(animLength/2));
	}
}


function lerp(a, b, t){
	return new Point(a.x + (b.x - a.x) * t, a.y + (b.y - a.y) * t);
}